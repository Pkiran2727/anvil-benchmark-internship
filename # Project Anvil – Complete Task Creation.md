# Project Anvil – Complete Task Creation Guide

## 1. Basic Requirements

Before starting, make sure you understand the core rules:

* Code must be **100% original**
* **No LLM / AI tools are allowed**
* Each **repository must contain at least 10 tasks**
* Each **task must include at least 6 tests**
* Tasks must be **challenging enough for AI agents**

Difficulty target:

AI agents should pass approximately **1–3 out of 5 runs**.



---

# 2. Install Environment

Install the **Anvil CLI**

```bash
uv sync
```

Set your DockerHub credentials:

```bash
echo "REGISTRY_USERNAME=your-dockerhub-username" >> .env
echo "REGISTRY_PASSWORD=your-dockerhub-password" >> .env
```

---

# 3. Initialize the Dataset

Create a dataset for your tasks:

```bash
anvil init-dataset \
--dataset my-dataset \
--repo-path /path/to/your/repo \
--base-image python:3.12
```

Example base images:

* python:3.12
* golang:1.22
* node:20

---

# 4. Generated Project Structure

After initialization the dataset will look like this:

```
my-dataset/
├── Dockerfile
├── requirements.txt
├── my-repo/
├── task-1/
│   ├── Dockerfile
│   ├── instance_info.txt
│   ├── run_script.sh
│   ├── task_tests.py
│   ├── parser.py
│   └── tasks.csv
├── task-2/
```

---

# 5. Write the Problem Statement

Create a file called **problem.md**

Example:

```
Task: Add User Profile Endpoint

Implement a GET /api/profile endpoint.

Requirements:
1. Add GetProfile method in service
2. Implement the method
3. Add controller handler
4. Register route

Return codes:

401 → if user not authenticated
404 → if user not found
```

Important rule:

The **problem statement is the single source of truth**.
Tests must check **exactly what the instructions describe**.

---

# 6. Write Tests (Minimum 6)

Tests should check **behavior**, not implementation details.

Correct example:

```python
def test_returns_401_when_unauthenticated():
    result = subprocess.run(...)
    assert result.stdout.strip() == "401"
```

Wrong example:

```python
assert "GetProfile" in service.go
```

Why?

The AI agent might implement the same functionality using **different method names or structure**.

---

# 7. Add the Task

Create the task using the capture-diff workflow:

```bash
anvil add-task -d my-dataset \
--problem-file problem.md \
--tests-file tests.py \
--capture-diff
```

The wizard will show:

```
Make your changes to the repository
Type 'done'
```

Steps:

1. Open the repository
2. Implement the solution code
3. Type **done** in the terminal

The system will:

* Capture the **git diff**
* Reset the repository for the next task

---

# 8. Test Classification

There are two types of tests.

## FAIL_TO_PASS

Tests for **new functionality**.

Before patch → FAIL
After patch → PASS

Example:

```
--fail-to-pass "test_new_feature"
```

---

## PASS_TO_PASS

Regression tests for **existing functionality**.

Before patch → PASS
After patch → PASS

Example:

```
--pass-to-pass "test_existing_feature"
```

---

# 9. Validate the Dataset

Run validation:

```bash
anvil validate-dataset -d my-dataset
```

The validator checks:

* Narrow tests
* Wide tests
* Behavior coverage
* Docstrings
* Typos
* Test isolation

---

# 10. Convert Dataset to Anvil Format

```bash
anvil convert-dataset \
-d my-dataset \
-u your-username \
--dockerhub-repo anvil-images
```

This generates:

* instances.yaml
* gold_patches.json

---

# 11. Publish Docker Images

```bash
anvil publish-images \
-d my-dataset \
-u your-username \
--repo anvil-images
```

---

# 12. Verify with Oracle Agent

Run the oracle evaluation:

```bash
anvil run-evals \
-d my-dataset \
--agent oracle \
-u your-username \
--dockerhub-repo anvil-images
```

Expected result:

All tests **PASS**

---

# 13. Test with an AI Agent

```bash
anvil run-evals \
-d my-dataset \
--agent mini-swe-agent \
--model anthropic/claude-sonnet-4 \
-u your-username \
--dockerhub-repo anvil-images
```

Expected pass rate:

```
1/5
2/5
3/5
```

If:

4–5 passes → task too easy
0 passes → task too hard

---

# 14. Submit Tasks on the Platform


1. Create submission
2. Upload task ZIP
3. Validate files
4. Agent evaluation
5. Quality check
6. Review queue

---

# 15. Approval Requirements

For a task to be approved:

✔ Oracle test passes (100%)
✔ Null check passes (0% false positives)
✔ Agent passes **1–3 out of 5 runs**
✔ Quality score **8+**
✔ Minimum **6 tests per task**

---

# Important Rules

❌ Do not copy code from the internet
❌ Do not use GitHub code
❌ Do not use LLM tools

✔ Code must be **original**

Violation will result in **removal from Project Anvil**.

---