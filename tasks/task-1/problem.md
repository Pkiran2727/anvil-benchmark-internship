## Task: Add GET /api/profile Endpoint

Implement a `GET /api/profile` endpoint that returns the authenticated user's profile information.

### Requirements

1. The endpoint must be accessible at `GET /api/profile`
2. The request must include a valid JWT token in the `Authorization: Bearer <token>` header
3. If no token is provided, return HTTP **401**
4. If the token is invalid or expired, return HTTP **401**
5. If authenticated, return HTTP **200** with a JSON body containing the user's profile:
   - `id` (integer)
   - `username` (string)
   - `email` (string)
   - `bio` (string)
   - `created_at` (ISO 8601 string)

### Notes
- Use the existing `require_auth` decorator from `auth.py`
- Use the existing `User` model from `models.py`
- `g.user_id` is set by `require_auth` — use it to look up the user
