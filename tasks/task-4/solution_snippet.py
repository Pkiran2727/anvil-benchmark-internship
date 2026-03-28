"""Solution for Task 4: adds GET /api/users with pagination."""

@app.route("/api/users", methods=["GET"])
def get_users():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 100)
    pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "users": [u.to_dict() for u in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page,
    }), 200
