## Task: Add Rate Limiting to POST /api/auth/login

Implement rate limiting on the `POST /api/auth/login` endpoint to prevent brute-force attacks.

### Requirements

1. Allow a maximum of **5 login attempts per IP address per 60-second window**
2. When the limit is exceeded, return HTTP **429** with `{"error": "Rate limit exceeded. Try again later."}`
3. The limit resets after the 60-second window passes
4. Successful logins count toward the limit just like failed ones
5. `GET /api/items` and other endpoints must NOT be rate-limited
6. The rate limit state can be stored in-memory (no database required)

### Notes
- Use `request.remote_addr` to get the client IP
- Use a `collections.defaultdict` or similar in-memory store to track attempts
- You can use `datetime` for tracking the time window
