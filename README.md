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

## For sanity checking, in one terminal, you could do

```bash
docker compose up --build
```

In a seperate terminal, you could then do this

```bash
# Create a task
curl -s -X POST http://localhost:8000/tasks/ \
  -H 'Content-Type: application/json' \
  -d '{"title":"Sanity Task","priority":1}'

# List tasks
curl -s http://localhost:8000/tasks/

# Get by ID
curl -s http://localhost:8000/tasks/1/

# Update
curl -s -X PUT http://localhost:8000/tasks/1/ \
  -H 'Content-Type: application/json' \
  -d '{"completed": true}'

# Delete
curl -s -X DELETE http://localhost:8000/tasks/1/
```
