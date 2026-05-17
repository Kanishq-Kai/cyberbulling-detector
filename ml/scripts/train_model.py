"""
Model Training Script
Trains one Logistic Regression classifier per toxic category using TF-IDF features.
Saves vectorizer and models to ../saved_models/.

Usage:
    python train_model.py

Prerequisites:
    Run preprocess.py first.
"""

import os
import sys
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.pipeline import Pipeline

LABELS = ["toxic", "severe_toxic", "obscene", "threat", "insult", "hate_speech"]

DATA_DIR  = os.path.join(os.path.dirname(__file__), "..", "data")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "saved_models")


def load_data():
    path = os.path.join(DATA_DIR, "processed.csv")
    if not os.path.exists(path):
        print("❌  processed.csv not found. Run preprocess.py first.")
        sys.exit(1)
    df = pd.read_csv(path)
    df.dropna(subset=["clean_text"], inplace=True)
    df["clean_text"] = df["clean_text"].astype(str)
    return df


def train():
    os.makedirs(MODEL_DIR, exist_ok=True)
    print("📂  Loading processed data …")
    df = load_data()
    print(f"    {len(df):,} samples loaded")

    X = df["clean_text"].values

    print("\n🔤  Fitting TF-IDF vectorizer …")
    vectorizer = TfidfVectorizer(
        max_features=50_000,
        ngram_range=(1, 2),
        min_df=3,
        max_df=0.95,
        sublinear_tf=True,
    )
    X_tfidf = vectorizer.fit_transform(X)
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"))
    print(f"    Vocabulary size: {len(vectorizer.vocabulary_):,}")

    results = {}
    for label in LABELS:
        if label not in df.columns:
            print(f"⚠️   Label '{label}' not in dataset, skipping.")
            continue

        y = df[label].values
        X_tr, X_val, y_tr, y_val = train_test_split(
            X_tfidf, y, test_size=0.15, random_state=42, stratify=y
        )

        print(f"\n🤖  Training [{label}]  (pos={y.sum():,} / {len(y):,})")

        # Class-weight balancing handles label imbalance
        clf = LogisticRegression(
            C=5.0,
            max_iter=1000,
            solver="lbfgs",
            class_weight="balanced",
            n_jobs=-1,
        )
        clf.fit(X_tr, y_tr)

        y_prob = clf.predict_proba(X_val)[:, 1]
        auc    = roc_auc_score(y_val, y_prob)
        print(f"    ROC-AUC: {auc:.4f}")
        print(classification_report(y_val, (y_prob >= 0.5).astype(int), target_names=["clean", label]))

        save_path = os.path.join(MODEL_DIR, f"model_{label}.pkl")
        joblib.dump(clf, save_path)
        results[label] = auc

    print("\n✅  Training complete!")
    print("\n📊  Summary:")
    for label, auc in results.items():
        print(f"    {label:15s}  AUC = {auc:.4f}")

    return results


if __name__ == "__main__":
    train()
