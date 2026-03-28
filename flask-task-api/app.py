"""Flask Task API — base application.

BASE STATE: Only register, login, get_items, create_item are implemented.
Tasks 1-10 add new endpoints to this file.
"""
import os
from flask import Flask, request, jsonify, g
from models import db, User, Item
from auth import create_token, require_auth


def create_app(config: dict = None) -> Flask:
    app = Flask(__name__)

    # ── Config ────────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config:
        app.config.update(config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ── Auth routes ───────────────────────────────────────────────

    @app.route("/api/auth/register", methods=["POST"])
    def register():
        data = request.get_json() or {}
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not username or not email or not password:
            return jsonify({"error": "username, email and password are required"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already taken"}), 409

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 409

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User created successfully", "id": user.id}), 201

    @app.route("/api/auth/login", methods=["POST"])
    def login():
        data = request.get_json() or {}
        username = data.get("username", "")
        password = data.get("password", "")

        if not username or not password:
            return jsonify({"error": "username and password required"}), 400

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_token(user.id, app.config["SECRET_KEY"])
        return jsonify({"token": token, "user_id": user.id}), 200

    # ── Items routes ──────────────────────────────────────────────

    @app.route("/api/items", methods=["GET"])
    def get_items():
        items = Item.query.all()
        return jsonify([i.to_dict() for i in items]), 200

    @app.route("/api/items", methods=["POST"])
    @require_auth
    def create_item():
        data = request.get_json() or {}
        name = data.get("name", "").strip()

        if not name:
            return jsonify({"error": "name is required"}), 400

        item = Item(
            name=name,
            description=data.get("description", ""),
            user_id=g.user_id,
        )
        db.session.add(item)
        db.session.commit()
        return jsonify(item.to_dict()), 201

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, host="0.0.0.0", port=5000)
