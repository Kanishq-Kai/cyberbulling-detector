"""
Model Evaluation Script
Loads saved models and prints detailed evaluation metrics.

Usage:
    python evaluate_model.py
"""

import os
import sys
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import (
    roc_auc_score, f1_score, precision_score, recall_score,
    confusion_matrix, classification_report
)

LABELS    = ["toxic", "severe_toxic", "obscene", "threat", "insult", "hate_speech"]
DATA_DIR  = os.path.join(os.path.dirname(__file__), "..", "data")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "saved_models")


def main():
    df_path  = os.path.join(DATA_DIR, "processed.csv")
    vec_path = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")

    if not os.path.exists(df_path) or not os.path.exists(vec_path):
        print("❌  Run preprocess.py and train_model.py first.")
        sys.exit(1)

    df  = pd.read_csv(df_path).dropna(subset=["clean_text"])
    vec = joblib.load(vec_path)
    X   = vec.transform(df["clean_text"].astype(str).values)

    print("=" * 55)
    print("  MODEL EVALUATION REPORT")
    print("=" * 55)

    for label in LABELS:
        path = os.path.join(MODEL_DIR, f"model_{label}.pkl")
        if not os.path.exists(path) or label not in df.columns:
            continue

        clf    = joblib.load(path)
        y_true = df[label].values
        y_prob = clf.predict_proba(X)[:, 1]
        y_pred = (y_prob >= 0.5).astype(int)

        print(f"\n🏷  {label.upper()}")
        print(f"   AUC-ROC   : {roc_auc_score(y_true, y_prob):.4f}")
        print(f"   F1-Score  : {f1_score(y_true, y_pred, zero_division=0):.4f}")
        print(f"   Precision : {precision_score(y_true, y_pred, zero_division=0):.4f}")
        print(f"   Recall    : {recall_score(y_true, y_pred, zero_division=0):.4f}")
        cm = confusion_matrix(y_true, y_pred)
        print(f"   Confusion Matrix:\n   {cm}")

    print("\n✅  Evaluation complete.")


if __name__ == "__main__":
    main()
