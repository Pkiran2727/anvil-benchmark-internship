"""Solution for Task 8: adds rate limiting to POST /api/auth/login.
Add these at the top of create_app() scope, and apply decorator to login().
"""

# Add at module level (before create_app):
from collections import defaultdict
from datetime import datetime, timedelta

_rate_store: dict = defaultdict(list)

def _check_rate_limit(ip: str, max_req: int = 5, window: int = 60) -> bool:
    """Returns True if request is allowed, False if rate limit exceeded."""
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=window)
    _rate_store[ip] = [t for t in _rate_store[ip] if t > cutoff]
    if len(_rate_store[ip]) >= max_req:
        return False
    _rate_store[ip].append(now)
    return True

# Then inside create_app(), modify the login route:
@app.route("/api/auth/login", methods=["POST"])
def login():
    if not _check_rate_limit(request.remote_addr):
        return jsonify({"error": "Rate limit exceeded. Try again later."}), 429

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
