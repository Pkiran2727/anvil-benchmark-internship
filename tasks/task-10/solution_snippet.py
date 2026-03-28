"""Solution for Task 10: adds GET /api/health endpoint."""

@app.route("/api/health", methods=["GET"])
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"
    return jsonify({
        "status": "ok" if db_status == "ok" else "degraded",
        "database": db_status,
    }), 200
