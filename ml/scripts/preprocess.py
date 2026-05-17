"""
Dataset Preprocessing Script
Reads Jigsaw train.csv, cleans text, saves processed CSV.

Usage:
    python preprocess.py

Input:  ../data/train.csv     (Jigsaw Toxic Comment dataset)
Output: ../data/processed.csv
"""

import os
import sys
import pandas as pd
import re
import string
import nltk

# ── NLTK setup ────────────────────────────────────────────────────────────────
for pkg in ["stopwords", "punkt", "wordnet", "omw-1.4"]:
    try:
        nltk.data.find(f"corpora/{pkg}" if pkg != "punkt" else f"tokenizers/{pkg}")
    except LookupError:
        nltk.download(pkg, quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

STOP_WORDS  = set(stopwords.words("english"))
lemmatizer  = WordNetLemmatizer()

LABELS = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]


def clean(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in STOP_WORDS and len(t) > 1]
    return " ".join(tokens)


def main():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    input_path  = os.path.join(data_dir, "train.csv")
    output_path = os.path.join(data_dir, "processed.csv")

    if not os.path.exists(input_path):
        print(f"❌  train.csv not found at {input_path}")
        print("    Download it from: https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge")
        sys.exit(1)

    print("📂  Loading dataset …")
    df = pd.read_csv(input_path)
    print(f"    Rows: {len(df):,}  |  Columns: {list(df.columns)}")

    print("🧹  Cleaning text …")
    df["clean_text"] = df["comment_text"].apply(clean)

    # Rename identity_hate → hate_speech for consistency with our API
    if "identity_hate" in df.columns:
        df.rename(columns={"identity_hate": "hate_speech"}, inplace=True)

    keep_cols = ["comment_text", "clean_text"] + [
        l.replace("identity_hate","hate_speech") for l in LABELS
    ]
    df = df[[c for c in keep_cols if c in df.columns]]
    df.dropna(subset=["clean_text"], inplace=True)
    df = df[df["clean_text"].str.len() > 3]

    os.makedirs(data_dir, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅  Processed CSV saved to {output_path}  ({len(df):,} rows)")

    # Label distribution
    labels_in_df = [l.replace("identity_hate","hate_speech") for l in LABELS if l.replace("identity_hate","hate_speech") in df.columns]
    print("\n📊  Label distribution:")
    for label in labels_in_df:
        pos = df[label].sum()
        print(f"    {label:15s}  {pos:6,}  ({pos/len(df)*100:.1f}%)")


if __name__ == "__main__":
    main()
