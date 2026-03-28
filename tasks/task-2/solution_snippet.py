"""Solution for Task 2: adds PUT /api/profile endpoint."""

@app.route("/api/profile", methods=["PUT"])
@require_auth
def update_profile():
    user = User.query.get(g.user_id)
    data = request.get_json() or {}

    if "email" in data:
        existing = User.query.filter_by(email=data["email"]).first()
        if existing and existing.id != user.id:
            return jsonify({"error": "Email already in use"}), 409
        user.email = data["email"]

    if "bio" in data:
        user.bio = data["bio"]

    db.session.commit()
    return jsonify(user.to_dict()), 200
