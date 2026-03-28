## Task: Add POST /api/auth/refresh Endpoint

Implement a `POST /api/auth/refresh` endpoint that accepts a valid JWT and returns a new JWT with a fresh expiry.

### Requirements

1. The endpoint must be accessible at `POST /api/auth/refresh`
2. Requires a valid JWT Bearer token (return **401** if missing/invalid)
3. On success:
   - Generate a new JWT for the same `user_id` with a fresh 24-hour expiry
   - Return HTTP **200** with `{"token": "<new_jwt>"}`
4. The new token must be different from the original (new `iat`/`exp` claims)
5. The new token must be valid and usable for authenticated requests

### Notes
- Use `require_auth` decorator — `g.user_id` will be set
- Call `create_token(g.user_id, current_app.config["SECRET_KEY"])` from `auth.py`
