# 🛠️ Project Anvil: Custom SWE-Bench Dataset

This repository contains a fully automated benchmark for evaluating AI Software Engineering agents (SWE agents). It features a custom Flask REST API and 11 unique coding tasks of varying difficulty.

## 🚀 Benchmark Overview
- **Base Environment**: Flask, SQLAlchemy, JWT Authentication, SQLite.
- **Task Count**: 11 unique coding challenges.
- **Verification**: 100% solvable by an Oracle agent (verified via Anvil CLI).
- **Calibration**: Gemini 2.0 Flash achieves ~36.4% success rate, indicating a meaningful difficulty curve.

**GitHub Repository**: [https://github.com/Pkiran2727/anvil-benchmark-internship](https://github.com/Pkiran2727/anvil-benchmark-internship)

## 📂 Repository Structure
- `flask-task-api/`: The base source code repository (The "Subject").
- `tasks/`: 11 task definitions including problem statements, behavioral tests, and golden patches.
- `add_tasks.py`: Automation script to inject solutions and register tasks in Anvil.

## 🛠️ How to Run
1. **Prerequisites**: Install the [Anvil CLI](https://github.com/AfterQuery/anvil).
2. **Initialize Dataset**:
   ```bash
   anvil init-dataset -d my-dataset --repo-path ./flask-task-api --base-image python:3.12
   ```
3. **Add Tasks**:
   ```bash
   python3 add_tasks.py
   ```
4. **Convert & Evaluate**:
   ```bash
   anvil convert-dataset -d my-dataset -u <dockerhub-username>
   anvil run-evals --dataset my-dataset --agent oracle
   ```

## 📊 Evaluation Insights
| Agent | pass@1 | Status |
| :--- | :--- | :--- |
| **Oracle** | 100.0% | ✅ Solvable |
| **Gemini 2.0 Flash (001)** | 36.4% | ⚠️ Challenging |

---
*Created as part of the Project Anvil Internship.*
