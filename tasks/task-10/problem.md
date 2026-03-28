## Task: Add GET /api/health Endpoint

Implement a `GET /api/health` endpoint that reports the health status of the application and its database connection.

### Requirements

1. The endpoint must be accessible at `GET /api/health`
2. No authentication required
3. The endpoint must check whether the database is reachable by executing a simple query (e.g., `SELECT 1`)
4. Return HTTP **200** in all cases (even if DB is down) with JSON:
   ```json
   { "status": "ok", "database": "ok" }
   ```
   or if DB fails:
   ```json
   { "status": "degraded", "database": "error" }
   ```
5. `status` must be `"ok"` when database is `"ok"`, and `"degraded"` when database is `"error"`

### Notes
- Use `db.session.execute(db.text("SELECT 1"))` inside a try/except
- Wrap the entire DB check in a try/except to handle connection errors
