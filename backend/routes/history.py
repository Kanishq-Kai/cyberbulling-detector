"""GET /history — paginated comment history."""
from flask import Blueprint, request, jsonify
from models.db import get_comments_collection

history_bp = Blueprint("history", __name__)

@history_bp.route("/history", methods=["GET"])
def history():
    page     = max(1, int(request.args.get("page", 1)))
    per_page = min(50, int(request.args.get("per_page", 20)))
    skip     = (page - 1) * per_page

    try:
        col   = get_comments_collection()
        total = col.count_documents({})
        docs  = list(col.find({}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(per_page))
        # Convert datetime to ISO string
        for d in docs:
            if "created_at" in d and hasattr(d["created_at"], "isoformat"):
                d["created_at"] = d["created_at"].isoformat()
        return jsonify({"total": total, "page": page, "per_page": per_page, "comments": docs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
