# Task Management API (FastAPI + SQLite)

A small, clean FastAPI service for managing tasks.

## Run (no Docker)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

```

## Run (with Docker)

```bash
# build image and start container
docker compose up --build
# visit: http://localhost:8000/docs

```

## To run tests, do this:

```bash
docker compose run --rm api pytest -q
```
