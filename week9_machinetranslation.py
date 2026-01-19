# ============================================================
# ENGLISH → FRENCH TRANSLATION USING HUGGING FACE TRANSFORMERS
# ============================================================
# This script demonstrates how to perform English-to-French translation 
# using a pre-trained model from the Hugging Face Transformers library.
# ============================================================

# -------------------------------
# 1. Import Required Library
# -------------------------------
# The 'pipeline' API makes it easy to perform NLP tasks like translation, 
# summarization, text generation, etc., with just a few lines of code.
from transformers import pipeline

# -------------------------------
# 2. Load Translation Pipeline
# -------------------------------
# Task: "translation_en_to_fr" (English to French)
# Model: "Helsinki-NLP/opus-mt-en-fr" (a widely used model for machine translation)
translator = pipeline(
    "translation_en_to_fr", 
    model="Helsinki-NLP/opus-mt-en-fr"
)

# -------------------------------
# 3. Perform Translation
# -------------------------------
# Provide English text as input; the model will return the French translation.
result = translator("Hello, what is your name?")

# -------------------------------
# 4. Display the Result
# -------------------------------
# The result is a list of dictionaries; each dictionary contains 'translation_text'.
print("French Translation:", result[0]['translation_text'])

# ============================================================
# END OF SCRIPT
# ============================================================
