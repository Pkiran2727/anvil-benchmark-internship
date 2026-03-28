"""Solution for Task 3: adds DELETE /api/account endpoint."""

@app.route("/api/account", methods=["DELETE"])
@require_auth
def delete_account():
    user = User.query.get(g.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted successfully"}), 200
