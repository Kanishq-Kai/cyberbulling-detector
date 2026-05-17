"""
Dataset Preprocessing Script
=============================
Preprocesses the Jigsaw Toxic Comment Classification Dataset.

Dataset: https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data
Place train.csv in ml/datasets/ before running.

Run: python preprocess_data.py
"""

import os
import re
import pickle
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required NLTK resources
print("Downloading NLTK resources...")
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("punkt_tab")

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
DATASET_PATH = "datasets/train.csv"
OUTPUT_PATH = "datasets/processed_data.pkl"
SAMPLE_SIZE = 50000  # Use a subset for faster training; set to None for full dataset

LABEL_COLUMNS = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

# ──────────────────────────────────────────────
# Text Preprocessing
# ──────────────────────────────────────────────
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text: str) -> str:
    """Full NLP preprocessing pipeline."""
    if not isinstance(text, str):
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # 3. Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # 4. Remove special characters and digits (keep letters only)
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # 5. Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # 6. Tokenize
    tokens = word_tokenize(text)

    # 7. Remove stopwords and short tokens
    tokens = [t for t in tokens if t not in stop_words and len(t) > 2]

    # 8. Lemmatization
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    return " ".join(tokens)


# ──────────────────────────────────────────────
# Load & Preprocess Dataset
# ──────────────────────────────────────────────
def load_and_preprocess():
    if not os.path.exists(DATASET_PATH):
        print(f"\n❌ Dataset not found at: {DATASET_PATH}")
        print("Please download the Jigsaw dataset from:")
        print("  https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data")
        print("Place train.csv in ml/datasets/ and re-run.\n")
        print("💡 Generating synthetic demo dataset for testing...")
        return generate_synthetic_dataset()

    print(f"Loading dataset from {DATASET_PATH}...")
    df = pd.read_csv(DATASET_PATH)

    if SAMPLE_SIZE:
        df = df.sample(n=min(SAMPLE_SIZE, len(df)), random_state=42)

    print(f"Dataset size: {len(df)} samples")
    print(f"Columns: {list(df.columns)}")
    print(f"\nLabel distribution:")
    for col in LABEL_COLUMNS:
        if col in df.columns:
            print(f"  {col}: {df[col].sum()} ({df[col].mean()*100:.1f}%)")

    print("\nPreprocessing text (this may take a few minutes)...")
    df["clean_text"] = df["comment_text"].apply(clean_text)

    # Rename identity_hate -> hate_speech for our API
    if "identity_hate" in df.columns:
        df = df.rename(columns={"identity_hate": "hate_speech"})

    label_cols = ["toxic", "severe_toxic", "obscene", "threat", "insult", "hate_speech"]
    available_labels = [c for c in label_cols if c in df.columns]

    X = df["clean_text"].values
    y = df[available_labels].values

    print(f"\n✅ Preprocessing complete!")
    print(f"   Features shape: {X.shape}")
    print(f"   Labels shape: {y.shape}")

    # Save processed data
    os.makedirs("datasets", exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        pickle.dump({"X": X, "y": y, "label_columns": available_labels}, f)

    print(f"   Saved to: {OUTPUT_PATH}")
    return X, y, available_labels


def generate_synthetic_dataset():
    """Generate a synthetic dataset for demo/testing when real dataset is unavailable."""
    print("Generating synthetic training data...")

    toxic_phrases = [
        "you are stupid and i hate you",
        "go kill yourself nobody likes you",
        "you are a complete idiot and loser",
        "i will hurt you if i see you",
        "you ugly disgusting piece of garbage",
        "everyone hates you including me",
        "you should be ashamed of yourself",
        "worthless trash get out of here",
        "shut up you moron nobody cares",
        "die in a fire you terrible person",
        "you are pathetic and weak",
        "i despise you completely and utterly",
        "you deserve to suffer",
        "nobody wants you here go away",
        "you are dumb and incompetent",
    ] * 200

    clean_phrases = [
        "i think this is a great idea",
        "thank you for sharing your thoughts",
        "i appreciate your perspective on this",
        "what a wonderful day it is today",
        "i disagree but respect your opinion",
        "this is very helpful information thank you",
        "could you please explain that further",
        "i found this really interesting",
        "great work on this project",
        "i look forward to hearing from you",
        "this makes a lot of sense to me",
        "wonderful explanation thank you so much",
        "i completely agree with you here",
        "this is exactly what i needed",
        "you explained that really well",
    ] * 200

    texts = toxic_phrases + clean_phrases
    n_toxic = len(toxic_phrases)
    n_clean = len(clean_phrases)

    labels = []
    for i in range(n_toxic):
        labels.append([1, 0, 0, 0, 1, 0])  # toxic + insult

    for i in range(n_clean):
        labels.append([0, 0, 0, 0, 0, 0])

    df = pd.DataFrame({"text": texts})
    df["clean_text"] = df["text"].apply(clean_text)

    X = df["clean_text"].values
    y = np.array(labels)
    label_columns = ["toxic", "severe_toxic", "obscene", "threat", "insult", "hate_speech"]

    os.makedirs("datasets", exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        pickle.dump({"X": X, "y": y, "label_columns": label_columns}, f)

    print(f"✅ Synthetic dataset generated: {len(X)} samples")
    print(f"   Saved to: {OUTPUT_PATH}")
    return X, y, label_columns


if __name__ == "__main__":
    X, y, labels = load_and_preprocess()
    print("\n🎯 Ready for model training. Run: python train_model.py")
