## Task: Add Pagination to GET /api/users

Implement a `GET /api/users` endpoint that returns a paginated list of all users.

### Requirements

1. The endpoint must be accessible at `GET /api/users`
2. No authentication required
3. Accept optional query parameters:
   - `page` (integer, default: 1) — page number (1-indexed)
   - `per_page` (integer, default: 10, max: 100) — users per page
4. Return HTTP **200** with JSON:
   ```json
   {
     "users": [ { "id": 1, "username": "...", "email": "...", "bio": "...", "created_at": "..." } ],
     "total": 50,
     "pages": 5,
     "current_page": 1
   }
   ```
5. `users` key must be an array of user objects (using `User.to_dict()`)
6. If `page` exceeds available pages, return empty `users` array (not an error)

### Notes
- Use Flask-SQLAlchemy's `.paginate()` method
- `total` = total number of users across all pages
