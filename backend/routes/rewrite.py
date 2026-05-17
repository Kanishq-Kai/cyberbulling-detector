"""POST /rewrite-comment — rule-based polite rephrasing (AI placeholder)."""
from flask import Blueprint, request, jsonify
import re

rewrite_bp = Blueprint("rewrite", __name__)

REPLACEMENTS = {
    r"\bidiot\b":   "someone I disagree with",
    r"\bstupid\b":  "mistaken",
    r"\bdumb\b":    "uninformed",
    r"\bloser\b":   "someone struggling",
    r"\bhate\b":    "strongly dislike",
    r"\bsuck\b":    "could improve",
    r"\bugly\b":    "visually different",
    r"\bfat\b":     "larger",
    r"\buseless\b": "not helpful in this context",
    r"\bworthless\b":"not currently valued",
    r"\bshut up\b": "please stop talking",
    r"\bidiot\b":   "uninformed person",
}

@rewrite_bp.route("/rewrite-comment", methods=["POST"])
def rewrite():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    rewritten = text
    flags = re.IGNORECASE
    for pattern, replacement in REPLACEMENTS.items():
        rewritten = re.sub(pattern, replacement, rewritten, flags=flags)

    # Generic polite wrapper if no specific replacement made
    if rewritten == text:
        rewritten = (
            "I respectfully disagree with this perspective. "
            "I think there might be a better way to express this viewpoint."
        )
    else:
        # Add polite prefix
        rewritten = rewritten[0].upper() + rewritten[1:]
        if not rewritten.endswith("."):
            rewritten += "."

    return jsonify({"original": text, "rewritten": rewritten}), 200
