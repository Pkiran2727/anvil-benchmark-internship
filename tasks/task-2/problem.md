## Task: Add PUT /api/profile Endpoint

Implement a `PUT /api/profile` endpoint that allows an authenticated user to update their profile.

### Requirements

1. The endpoint must be accessible at `PUT /api/profile`
2. Requires a valid JWT Bearer token (return **401** if missing/invalid)
3. Accept a JSON body with optional fields:
   - `bio` (string, max 500 chars) — update the user's bio
   - `email` (string) — update the user's email
4. If `email` is changed to one already used by another user, return **409**
5. On success, return HTTP **200** with the updated user profile JSON:
   - `id`, `username`, `email`, `bio`, `created_at`
6. Changes must persist to the database

### Notes
- Only update fields that are present in the request body
- Use `require_auth` decorator and `g.user_id` to identify the user
