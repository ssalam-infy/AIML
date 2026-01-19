"""week11.py
ML lifecycle demo:
1) Load dataset
2) Train + evaluate a classifier
3) (Notebook-only) simple interactive prediction UI using ipywidgets
4) Run Evidently data drift report and print the results in a readable form

Notes:
- The ipywidgets part is intended for Jupyter. When running as a plain .py script,
  VS Code/terminal will print a textual representation of the widgets.
- Evidently (0.7.x) returns a Snapshot from `Report.run()`. To inspect results,
  use `drift_result.dict()` and pretty-print it.
"""

# -----------------------------
# Imports
# -----------------------------

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pandas as pd
from evidently import Report, Dataset, DataDefinition
from evidently.presets import DataDriftPreset
from evidently.core.datasets import BinaryClassification

import numpy as np
import pandas as pd
from IPython.display import display, clear_output
import ipywidgets as widgets

# -----------------------------
# Evidently version (for debugging)
# -----------------------------

import evidently
print("Evidently version:", evidently.__version__)

# -----------------------------
# Step 2: Load Dataset
# -----------------------------

data = load_breast_cancer(as_frame=True)
df = data.frame
df['target'] = data.target
X = df.drop(columns='target')
y = df['target']

# -----------------------------
# Step 3: Data Splitting and Preprocessing
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# Step 4: Model Training
# -----------------------------

model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# -----------------------------
# Step 5: Evaluation
# -----------------------------

y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))

# -----------------------------
# Step 6: Deployment (ipywidgets demo)
# -----------------------------

# Create a widget for each feature
input_widgets = {col: widgets.FloatText(description=col, step=0.1) for col in X.columns}

# Output widget to show prediction result
output = widgets.Output()

# Prediction function
def predict_ipywidget(btn):
    with output:
        clear_output()
        try:
            # Gather inputs
            input_values = [input_widgets[col].value for col in X.columns]
            input_array = np.array(input_values).reshape(1, -1)
            input_scaled = scaler.transform(input_array)
            prediction = model.predict(input_scaled)[0]
            probability = model.predict_proba(input_scaled)[0][prediction]
            result = {
                "Malignant": float(1 - prediction),
                "Benign": float(prediction)
            }
            print("Prediction:", "Benign" if prediction == 1 else "Malignant")
            print("Probability:", round(probability * 100, 2), "%")
        except Exception as e:
            print("Error:", e)

# Button to trigger prediction
predict_button = widgets.Button(description="Predict")
predict_button.on_click(predict_ipywidget)

# Display everything
display(widgets.VBox(list(input_widgets.values()) + [predict_button, output]))


# -----------------------------
# Step 7: Data Drift Monitoring with Evidently
# -----------------------------

# Create reference and current datasets
reference_data = pd.DataFrame(X_train_scaled, columns=X.columns)
current_data = pd.DataFrame(X_test_scaled, columns=X.columns)

reference_data['target'] = y_train.values
current_data['target'] = y_test.values

# Add predicted class and predicted probabilities
reference_data['prediction_proba'] = model.predict_proba(X_train_scaled)[:, 1]
current_data['prediction_proba'] = model.predict_proba(X_test_scaled)[:, 1]

reference_data['prediction'] = (reference_data['prediction_proba'] >= 0.5).astype(int)
current_data['prediction'] = (current_data['prediction_proba'] >= 0.5).astype(int)


data_def = DataDefinition(
    classification=[
        BinaryClassification(
            column_name="target",
            predicted_column_name="prediction",
            prediction_probas_column_name="prediction_proba",
            options=[0, 1]
        )
    ]
)


ref_dataset = Dataset.from_pandas(reference_data, data_definition=data_def)
cur_dataset = Dataset.from_pandas(current_data, data_definition=data_def)

# Step 3: Create and run the Data Drift Report
# (Evidently returns a Snapshot object)
drift_report = Report(metrics=[DataDriftPreset()])
drift_result = drift_report.run(reference_data=ref_dataset, current_data=cur_dataset)
drift_result
# # -----------------------------
# # Display drift results (readable)
# # -----------------------------
# from pprint import pprint
# pprint(drift_result.dict(), width=120)


# import json

# report_data = drift_result.dict()

# html = f"""
# <html>
# <head><title>Evidently Drift Report (Snapshot)</title></head>
# <body>
# <h2>Evidently Drift Output (Snapshot dict)</h2>
# <pre>{json.dumps(report_data, indent=2, default=str)}</pre>
# </body>
# </html>
# """

# with open("drift_report.html", "w", encoding="utf-8") as f:
#     f.write(html)

# print("Saved HTML to drift_report.html (open it in a browser).")