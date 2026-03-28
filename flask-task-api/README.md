# Flask Task API

A minimal REST API built with Flask for Project Anvil evaluation tasks.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## Endpoints (base)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /api/auth/register | No | Register new user |
| POST | /api/auth/login | No | Login, returns JWT |
| GET | /api/items | No | List all items |
| POST | /api/items | Yes | Create item |

## Running Tests

```bash
pytest
```
