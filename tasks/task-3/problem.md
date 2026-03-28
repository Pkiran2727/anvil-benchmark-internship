## Task: Add DELETE /api/account Endpoint

Implement a `DELETE /api/account` endpoint that allows an authenticated user to permanently delete their account.

### Requirements

1. The endpoint must be accessible at `DELETE /api/account`
2. Requires a valid JWT Bearer token (return **401** if missing/invalid)
3. On success:
   - Delete the user record from the database
   - Cascade delete the user's items (already configured in the model)
   - Return HTTP **200** with `{"message": "Account deleted successfully"}`
4. After deletion, the user's token should no longer grant access

### Notes
- Use `require_auth` decorator and `g.user_id` to identify the user
- Use `db.session.delete(user)` followed by `db.session.commit()`
