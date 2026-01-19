# ===============================================================
# SENTIMENT ANALYSIS USING A PRETRAINED TRANSFORMER (HuggingFace)
# ===============================================================
# Note:
# - spaCy's `en_core_web_trf` is a general-purpose English pipeline (NER/POS/etc.)
#   and does NOT ship with an IMDb sentiment classifier (so `doc.cats['positive']`
#   won't be available).
# - For out-of-the-box sentiment classification, use a pretrained model from
#   HuggingFace Transformers.
# ===============================================================

# -------------------------------
# 1. Imports
# -------------------------------
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from transformers import pipeline

# -------------------------------
# 2. Load Sentiment Model (HF)
# -------------------------------
# This default pipeline loads a strong English sentiment model.
# Output example: {'label': 'POSITIVE', 'score': 0.999...}
sa = pipeline("sentiment-analysis")
print("Loaded HuggingFace sentiment-analysis pipeline")

# -------------------------------
# 3. Load the IMDb Dataset
# -------------------------------
# Using a local file avoids 404/network issues.
# Place the file 'IMDB Dataset.csv' in this project folder.

df = pd.read_csv("IMDB Dataset.csv")
print("Loaded dataset", df.shape)

# Map labels to numeric targets.
df["sentiment"] = df["sentiment"].map({"positive": 1, "negative": 0})

# -------------------------------
# 4. Split Data into Train and Test Sets
# -------------------------------
X = df["review"]
y = df["sentiment"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# 5. Define Prediction Function
# -------------------------------
def predict_label(text: str) -> int:
    # Keep text length reasonable for performance (IMDb reviews can be very long).
    # The model will truncate internally; we also do a small pre-trim to avoid
    # extreme tokenization cost.
    text = text.strip()
    if len(text) > 4000:
        text = text[:4000]

    out = sa(text, truncation=True)[0]
    label = out["label"].upper()
    return 1 if label == "POSITIVE" else 0

# -------------------------------
# 6. Evaluate
# -------------------------------
print("Starting predictions...")
# If you want faster runs, evaluate on a subset, e.g. X_test.iloc[:1000]
y_pred = [predict_label(t) for t in X_test]

print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Negative", "Positive"]))

# ===============================================================
# END OF SCRIPT
# ===============================================================
