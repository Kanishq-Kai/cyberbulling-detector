"""
MongoDB connection and collection helpers
"""
import os
from pymongo import MongoClient
from datetime import datetime

_client = None
_db = None

def get_db():
    global _client, _db
    if _db is None:
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/toxicdb")
        _client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        _db = _client.get_default_database()
    return _db

def get_comments_collection():
    return get_db()["comments"]

# ── Schema helper ─────────────────────────────────────────────────────────────
def build_comment_doc(text, result, rewritten=None):
    """Build a MongoDB document from prediction result."""
    return {
        "text": text,
        "toxicity_score": result.get("toxicity_score", 0),
        "is_toxic": result.get("is_toxic", False),
        "sentiment": result.get("sentiment", "neutral"),
        "categories": result.get("categories", {}),
        "confidence": result.get("confidence", 0),
        "rewritten": rewritten,
        "created_at": datetime.utcnow(),
    }
