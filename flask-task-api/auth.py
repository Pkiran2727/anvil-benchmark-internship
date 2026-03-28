"""JWT authentication helpers."""
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify, g, current_app


def create_token(user_id: int, secret_key: str, expires_in: int = 86400) -> str:
    """Create a signed JWT. expires_in is in seconds (default 24h)."""
    payload = {
        "user_id": user_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


def verify_token(token: str, secret_key: str):
    """Decode and verify a JWT. Returns user_id or None on failure."""
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload["user_id"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def require_auth(f):
    """Route decorator: requires valid Bearer token in Authorization header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authentication required"}), 401
        token = auth_header[7:]  # strip "Bearer "
        user_id = verify_token(token, current_app.config["SECRET_KEY"])
        if user_id is None:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Check if user exists in DB (required for Task 3)
        from models import User
        if not User.query.get(user_id):
            return jsonify({"error": "User no longer exists"}), 401
            
        g.user_id = user_id
        return f(*args, **kwargs)
    return decorated
