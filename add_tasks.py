import os
import subprocess
import shutil

BASE_DIR = "/Content/AI-PROJECTS/AI Internship/Internship1"
REPO_DIR = os.path.join(BASE_DIR, "flask-task-api")
TASKS_DIR = os.path.join(BASE_DIR, "tasks")
ANVIL_DIR = os.path.join(BASE_DIR, "anvil-cli")

def main():
    os.chdir(REPO_DIR)
    
    # Ensure git is clean
    subprocess.run(["git", "checkout", "."], check=True)
    subprocess.run(["git", "clean", "-fd"], check=True)

    app_py_path = os.path.join(REPO_DIR, "app.py")
    
    for i in range(1, 11):
        task_name = f"task-{i}"
        task_dir = os.path.join(TASKS_DIR, task_name)
        
        print(f"--- Processing {task_name} ---")
        
        # 1. Back up app.py
        with open(app_py_path, "r") as f:
            original_app_code = f.read()
            
        # 2. Add solution snippet to app.py
        snippet_path = os.path.join(task_dir, "solution_snippet.py")
        with open(snippet_path, "r") as f:
            snippet = f.read()
            
        with open(app_py_path, "a") as f:
            if i in [5, 8]:
                # Special inserts for task 5 and 8 that go at the top
                # (handled directly in the manual edit process below)
                pass
            f.write("\n" + snippet)
            
        # TASK SPECIFIC INJECTIONS
        if i == 5:
            # Task 5: Add import re at top, and insert check in register()
            new_code = original_app_code.replace(
                "import os",
                "import os\nimport re\nEMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}$')"
            )
            new_code = new_code.replace(
                'if not username or not email or not password:\n            return jsonify({"error": "username, email and password are required"}), 400',
                'if not username or not email or not password:\n            return jsonify({"error": "username, email and password are required"}), 400\n\n        if not EMAIL_RE.match(email):\n            return jsonify({"error": "Invalid email format"}), 400'
            )
            with open(app_py_path, "w") as f: f.write(new_code)
            
        elif i == 7:
            # Task 7 replaces get_items
            new_code = original_app_code.replace(
                '@app.route("/api/items", methods=["GET"])\n    def get_items():\n        items = Item.query.all()\n        return jsonify([i.to_dict() for i in items]), 200',
                '@app.route("/api/items", methods=["GET"])\n    def get_items():\n        q = request.args.get("q", "").strip()\n        if q:\n            items = Item.query.filter(Item.name.ilike(f"%{q}%")).all()\n        else:\n            items = Item.query.all()\n        return jsonify([i.to_dict() for i in items]), 200'
            )
            with open(app_py_path, "w") as f: f.write(new_code)
            
        elif i == 8:
            # Task 8 adds rate limiter at top, replaces login
            new_code = original_app_code.replace(
                "import os",
                "import os\nfrom collections import defaultdict\nfrom datetime import datetime, timedelta"
            )
            # Insert helper inside create_app
            rate_limit_helper = """
    app.rate_store = defaultdict(list)
    def _check_rate_limit(ip, max_req=5, window=60):
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=window)
        app.rate_store[ip] = [t for t in app.rate_store[ip] if t > cutoff]
        if len(app.rate_store[ip]) >= max_req:
            return False
        app.rate_store[ip].append(now)
        return True
"""
            new_code = new_code.replace("db.init_app(app)", "db.init_app(app)" + rate_limit_helper)
            new_code = new_code.replace(
                '@app.route("/api/auth/login", methods=["POST"])\n    def login():\n        data = request.get_json() or {}',
                '@app.route("/api/auth/login", methods=["POST"])\n    def login():\n        if not _check_rate_limit(request.remote_addr):\n            return jsonify({"error": "Rate limit exceeded. Try again later."}), 429\n        data = request.get_json() or {}'
            )
            with open(app_py_path, "w") as f: f.write(new_code)
            
        elif i == 9:
            # Task 9 adds audit logs to register and create_item
            new_code = original_app_code.replace(
                'from models import db, User, Item',
                'from models import db, User, Item, AuditLog'
            )
            new_code = new_code.replace(
                'db.session.add(user)\n        db.session.commit()',
                'db.session.add(user)\n        db.session.commit()\n        db.session.add(AuditLog(action="register", resource="user", user_id=None))\n        db.session.commit()'
            )
            new_code = new_code.replace(
                'db.session.add(item)\n        db.session.commit()',
                'db.session.add(item)\n        db.session.commit()\n        db.session.add(AuditLog(action="create_item", resource="item", user_id=g.user_id))\n        db.session.commit()'
            )
            # Use correctly indented snippet for the audit endpoint
            indented_snippet = "\n".join(["    " + line for line in snippet.splitlines()])
            new_code = new_code.replace("    return app", f"{indented_snippet}\n\n    return app")
            with open(app_py_path, "w") as f: f.write(new_code)

        elif i in [1, 2, 3, 4, 6, 10]:
            # Indent the snippet correctly (4 spaces)
            indented_snippet = "\n".join(["    " + line for line in snippet.splitlines()])
            # Insert before 'return app'
            new_code = original_app_code.replace(
                "    return app",
                f"{indented_snippet}\n\n    return app"
            )
            with open(app_py_path, "w") as f: f.write(new_code)

        # 3. Generate the git patch
        patch_path = os.path.join(task_dir, "solution.diff")
        with open(patch_path, "w") as f:
            subprocess.run(["git", "diff"], stdout=f, check=True)
            
        os.chdir(ANVIL_DIR)
        
        # 4. Add task to Anvil dataset
        cmd = [
            "uv", "run", "anvil", "add-task",
            "-d", "my-dataset",
            "--problem-file", os.path.join(task_dir, "problem.md"),
            "--tests-file", os.path.join(task_dir, "tests.py"),
            "--patch-file", patch_path
        ]
        
        # Remove task if exists to avoid task-21 etc
        task_id = f"flask-task-api.task-{i}"
        # (This is handled by our manual cleanup below)
        
        if i == 5:
            # For task 5, tell Anvil the fail-to-pass tests explicitly if needed
            # (Anvil might auto-detect these, but we can just run the command)
            pass
            
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print("ERROR:")
            print(result.stderr)
            break
            
        # 5. Reset app.py for next task
        os.chdir(REPO_DIR)
        subprocess.run(["git", "checkout", "app.py"], check=True)

if __name__ == "__main__":
    main()
