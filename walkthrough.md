# Project Anvil: Internship Milestone Complete

This document summarizes the successful creation and validation of a 10-task coding benchmark for Project Anvil.

## 🏆 Final Results
- **Tasks Created**: 10 original coding challenges
- **Base Repo**: Flask REST API with JWT Auth + SQLAlchemy
- **Validation**: **100% Pass Rate** using the `oracle` agent.
- **Environment**: Fully automated Docker Hub integration (`anvil-images-v6`)

## 🏗️ Project Architecture

The project is organized into four main layers:

### 1. Repository Layer (`flask-task-api/`)
This is the heart of the system. It contains the base application code that agents must modify.
- `app.py`: The Flask app entry point. Includes the `create_app` factory and endpoints for registration, login, and items.
- `models.py`: Defines the `User`, `Item`, and `AuditLog` database models using SQLAlchemy.
- `auth.py`: Implements JWT-based authentication with a secure `require_auth` decorator that verifies both the token and user existence.

### 2. Task Definition Layer (`tasks/`)
We meticulously designed 10 tasks of increasing difficulty:
- **Task 1-4**: Basic Refactoring (User Profiles, Authentication, Pagination).
- **Task 5-7**: Logic Impl (Email Validation, Token Refresh, Smart Search).
- **Task 8-10**: Advanced Features (Rate Limiting, Audit Logs, Health Checks).

Each task includes:
- `problem.md`: Clear instructions for the AI agent.
- `tests.py`: 6+ behavioral tests to verify the solution.
- `solution_snippet.py`: The "Gold Pattern" for injection.

### 3. Automation Layer (`add_tasks.py`)
This Python script automates the tedious work of registering tasks with Anvil:
1. Resets the repo to a clean state.
2. Injects the solution snippet into `app.py`.
3. Records a `git diff` as the "Gold Patch".
4. Registers the task with `anvil add-task`.

### 4. Anvil Engine Layer (`anvil-cli/`)
- `anvil convert-dataset`: Generates the final CSV/YAML/JSON configuration.
- `anvil publish-images`: Builds and pushes 11 Docker images (1 base + 10 instances) to Docker Hub.
- `anvil run-evals`: Runs the agent inside the container on Modal.com.

## 🎬 Execution Flow (How it works)

When you run an evaluation, here is exactly what happens:
1. **Instantiation**: Anvil pulls the Docker image for the specific task from `trustnoonebeonlyone/anvil-images-v6`.
2. **Setup**: The container starts with the "Base State" of your repo.
3. **Rollout**: 
   - **Oracle**: Applies your pre-recorded "Gold Patch" perfectly.
   - **LLM Agent**: Reads the `problem.md` and tries to write the code itself.
4. **Verification**: After the code is modified, Anvil runs `pytest` on the `tests.py` file included in that container.
5. **Score**: If all tests pass, the task is marked as Successful.

## 📸 Validation Proof

```text
  Task                                     Result       pass@1  
  ───────────────────────────────────────────────────────────────────────
  flask-task-api.task-1                    █████ 1/1      100%    ✓
  flask-task-api.task-2                    █████ 1/1      100%    ✓
  flask-task-api.task-3                    █████ 1/1      100%    ✓
  ...
  flask-task-api.task-10                   █████ 1/1      100%    ✓
═══════════════════════════════════════════════════════════════════════════
Final Result: 100.0% Pass Rate
```

---
**Status**: COMPLETED & READY FOR SUBMISSION
