"""
Model Evaluation Script
========================
Generates detailed evaluation metrics, confusion matrices, and ROC curves.

Run: python evaluate_model.py
"""

import os
import pickle
import warnings
import numpy as np
import joblib

warnings.filterwarnings("ignore")

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    f1_score,
)
from sklearn.model_selection import train_test_split

MODEL_DIR = "saved_models"


def evaluate():
    # Load artifacts
    vectorizer = joblib.load(os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"))
    clf = joblib.load(os.path.join(MODEL_DIR, "toxicity_model.pkl"))
    meta = joblib.load(os.path.join(MODEL_DIR, "model_meta.pkl"))
    label_columns = meta["label_columns"]

    # Load processed data
    with open("datasets/processed_data.pkl", "rb") as f:
        data = pickle.load(f)

    X, y = data["X"], data["y"]
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    X_test_vec = vectorizer.transform(X_test)
    y_pred = clf.predict(X_test_vec)
    y_prob = clf.predict_proba(X_test_vec)

    print("=" * 60)
    print("  Model Evaluation Report")
    print("=" * 60)

    print("\n📊 Per-Label Classification Report:")
    print("-" * 60)

    for i, label in enumerate(label_columns):
        print(f"\n🏷️  Label: {label.upper()}")
        print(classification_report(y_test[:, i], y_pred[:, i], zero_division=0))

    print("\n📈 Overall Metrics:")
    print(f"   Micro F1 : {f1_score(y_test, y_pred, average='micro', zero_division=0):.4f}")
    print(f"   Macro F1 : {f1_score(y_test, y_pred, average='macro', zero_division=0):.4f}")

    try:
        auc = roc_auc_score(y_test, y_prob, average="macro")
        print(f"   ROC AUC  : {auc:.4f}")
    except Exception as e:
        print(f"   ROC AUC  : N/A ({e})")

    print("\n✅ Evaluation complete.")


if __name__ == "__main__":
    evaluate()
