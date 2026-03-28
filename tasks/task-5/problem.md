## Task: Add Email Format Validation on Registration

Extend the `POST /api/auth/register` endpoint to validate that the provided `email` field is a properly formatted email address before creating the user.

### Requirements

1. Validate the `email` field format using a regular expression or equivalent check
2. A valid email must contain:
   - A local part (letters, digits, `._%+-`)
   - An `@` symbol
   - A domain part with at least one `.`
3. If the email format is invalid, return HTTP **400** with `{"error": "Invalid email format"}`
4. This check must happen **before** the duplicate email check
5. Valid emails must still result in HTTP **201** (normal registration succeeds)
6. Registration without an email still returns HTTP **400** (existing behavior preserved)

### Notes
- You can use Python's `re` module
- Example valid: `user@example.com`, `test.name+tag@sub.domain.org`
- Example invalid: `notanemail`, `@nodomain`, `missing@`, `user@.com`
