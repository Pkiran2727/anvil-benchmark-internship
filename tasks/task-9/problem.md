## Task: Add Audit Logging for Write Operations

Add an audit log system that records all user write operations (POST and DELETE requests that modify data).

### Requirements

1. Use the existing `AuditLog` model in `models.py` (fields: `id`, `user_id`, `action`, `resource`, `timestamp`)
2. Log an entry **after** each of these operations succeeds:
   - `POST /api/auth/register` → action=`"register"`, resource=`"user"`, user_id=`None`
   - `POST /api/items` → action=`"create_item"`, resource=`"item"`, user_id=current user
   - `DELETE /api/account` → action=`"delete_account"`, resource=`"user"`, user_id=deleted user's id
3. Implement a new `GET /api/audit` endpoint that:
   - Requires authentication (Bearer token)
   - Returns HTTP **200** with a JSON array of audit log entries in reverse chronological order
   - Each entry: `{"id", "user_id", "action", "resource", "timestamp"}`

### Notes
- Import `AuditLog` from `models.py` where needed
- Use `db.session.add(AuditLog(...))` and `db.session.commit()` inside the route
