"""Solution for Task 6: adds POST /api/auth/refresh endpoint."""

@app.route("/api/auth/refresh", methods=["POST"])
@require_auth
def refresh_token():
    new_token = create_token(g.user_id, app.config["SECRET_KEY"])
    return jsonify({"token": new_token}), 200
