from __future__ import annotations
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import schemas, crud
from .deps import pagination_params

Base.metadata.create_all(bind=engine) # Create our tables on startup

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/tasks/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new task.

    - **title**: required, 1–255 chars
    - **description**: optional
    - **priority**: 1 (High), 2 (Medium), 3 (Low)
    - **due_date**: ISO 8601 datetime (optional)
    """
    task = crud.create_task(db, payload)
    return task

@app.get("/tasks/", response_model=List[schemas.TaskOut])
def list_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[int] = Query(None, ge=1, le=3, description="Filter by priority"),
    q: Optional[str] = Query(None, description="Search in title/description"),
    db: Session = Depends(get_db),
    pag=Depends(pagination_params),
):
    """
    List tasks with optional filters and pagination.

    Query params:
    - **completed**: bool
    - **priority**: 1..3
    - **q**: search substring in title/description (case-insensitive)
    - **page**, **page_size**: pagination controls
    """
    page, page_size = pag
    items, total = crud.list_tasks(db, completed, priority, q, page, page_size)


    response: Response = Response()
    response.headers["X-Total-Count"] = str(total)
    response.headers["X-Page"] = str(page)
    response.headers["X-Page-Size"] = str(page_size)
    return items

@app.get("/tasks/{task_id}/", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a task by **task_id**.
    """
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    return task

@app.put("/tasks/{task_id}/", response_model=schemas.TaskOut)
def update_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """
    Update a task (partial update allowed).

    Any field is optional:
    - **title**, **description**, **priority**, **due_date**, **completed**
    """
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    task = crud.update_task(db, task, payload)
    return task

@app.delete("/tasks/{task_id}/", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by **task_id**.
    """
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    crud.delete_task(db, task)
    return {"message": "Task deleted successfully."}

