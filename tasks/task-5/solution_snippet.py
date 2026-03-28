"""Solution for Task 5: adds email validation to register.
Add import re at top of app.py, and insert the validation check
inside register() before the duplicate-email check.
"""

# At top of app.py add:
import re
EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")

# Inside register(), after the blank-field check, add:
if not EMAIL_RE.match(email):
    return jsonify({"error": "Invalid email format"}), 400
