"""POST /predict — core toxicity prediction endpoint."""
from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from utils.preprocessor import preprocess
from utils.model_loader import predict as ml_predict
from models.db import get_comments_collection, build_comment_doc

predict_bp = Blueprint("predict", __name__)

SEVERITY_THRESHOLDS = {
    "safe":     (0.0,  0.15),
    "mild":     (0.15, 0.40),
    "moderate": (0.40, 0.65),
    "high":     (0.65, 0.85),
    "severe":   (0.85, 1.01),
}

def get_severity_label(score: float) -> str:
    for label, (lo, hi) in SEVERITY_THRESHOLDS.items():
        if lo <= score < hi:
            return label
    return "severe"


@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400
    if len(text) > 5000:
        return jsonify({"error": "Text too long (max 5000 chars)"}), 400

    preprocessed = preprocess(text)
    result = ml_predict(text, preprocessed)

    toxicity_score = result["toxicity_score"]
    is_toxic       = toxicity_score >= 0.35
    confidence     = round(toxicity_score * 100, 1)
    severity       = get_severity_label(toxicity_score)

    warning = None
    if severity == "severe":
        warning = "🚨 Extremely toxic content detected. This message could cause serious harm."
    elif severity == "high":
        warning = "⚠️ High toxicity detected. Please reconsider sending this message."
    elif severity == "moderate":
        warning = "⚠️ Moderate toxicity detected. Consider rephrasing."
    elif severity == "mild":
        warning = "💬 Mildly inappropriate content detected."

    response = {
        "text":            text,
        "toxicity_score":  toxicity_score,
        "is_toxic":        is_toxic,
        "severity":        severity,
        "confidence":      confidence,
        "sentiment":       result["sentiment"],
        "categories":      result["categories"],
        "warning":         warning,
        "model_used":      result.get("model_used"),
        "timestamp":       datetime.now(timezone.utc).isoformat(),
    }

    # Persist to MongoDB (non-blocking — ignore DB errors)
    try:
        col = get_comments_collection()
        col.insert_one(build_comment_doc(text, response))
    except Exception:
        pass

    return jsonify(response), 200
