"""
AI-Powered Cyberbullying & Toxic Comment Detection System
Main Flask Application Entry Point
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])

# ── Register blueprints ──────────────────────────────────────────────────────
from routes.predict   import predict_bp
from routes.history   import history_bp
from routes.analytics import analytics_bp
from routes.rewrite   import rewrite_bp

app.register_blueprint(predict_bp)
app.register_blueprint(history_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(rewrite_bp)

# ── Health check ─────────────────────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "Toxicity Detection API is running"}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    print(f"🚀 Server running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
