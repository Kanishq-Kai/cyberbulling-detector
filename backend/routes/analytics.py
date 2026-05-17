"""GET /analytics — aggregated dashboard data."""
from flask import Blueprint, jsonify
from models.db import get_comments_collection

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics", methods=["GET"])
def analytics():
    try:
        col   = get_comments_collection()
        total = col.count_documents({})
        toxic = col.count_documents({"is_toxic": True})
        safe  = total - toxic

        # Category distribution
        categories = ["toxic","severe_toxic","insult","threat","obscene","hate_speech"]
        cat_counts  = {}
        for cat in categories:
            cat_counts[cat] = col.count_documents({f"categories.{cat}": {"$gte": 0.5}})

        # Severity distribution
        severity_pipeline = [
            {"$group": {"_id": "$severity", "count": {"$sum": 1}}}
        ]
        severity_raw = list(col.aggregate(severity_pipeline))
        severity_dist = {r["_id"]: r["count"] for r in severity_raw if r["_id"]}

        # Sentiment distribution
        sentiment_pipeline = [
            {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}
        ]
        sentiment_raw  = list(col.aggregate(sentiment_pipeline))
        sentiment_dist = {r["_id"]: r["count"] for r in sentiment_raw if r["_id"]}

        # Recent 7 days trend (daily count)
        from datetime import datetime, timedelta, timezone
        trend = []
        for i in range(6, -1, -1):
            day_start = datetime.now(timezone.utc).replace(hour=0,minute=0,second=0,microsecond=0) - timedelta(days=i)
            day_end   = day_start + timedelta(days=1)
            count     = col.count_documents({"created_at": {"$gte": day_start, "$lt": day_end}})
            trend.append({"date": day_start.strftime("%b %d"), "count": count})

        return jsonify({
            "total":           total,
            "toxic":           toxic,
            "safe":            safe,
            "toxic_rate":      round(toxic / total * 100, 1) if total else 0,
            "category_dist":   cat_counts,
            "severity_dist":   severity_dist,
            "sentiment_dist":  sentiment_dist,
            "daily_trend":     trend,
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
