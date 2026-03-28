"""Solution for Task 9: adds GET /api/audit endpoint."""

@app.route("/api/audit", methods=["GET"])
@require_auth
def get_audit_log():
    from models import AuditLog
    logs = AuditLog.query.order_by(AuditLog.id.desc()).all()
    return jsonify([l.to_dict() for l in logs]), 200
