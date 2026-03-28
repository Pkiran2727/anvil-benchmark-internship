"""Solution for Task 1: adds GET /api/profile endpoint.
Append this block inside create_app(), after the login route.
"""

# ── Profile routes ─────────────────────────────────────────────────────────
# Task 1: GET /api/profile

@app.route("/api/profile", methods=["GET"])
@require_auth
def get_profile():
    user = User.query.get(g.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200
