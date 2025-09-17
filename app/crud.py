from __future__ import annotations
from typing import List, Optional, Tuple, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, func
from . import models, schemas

def create_task(db: Session, data: schemas.TaskCreate) -> models.Task:
    task = models.Task(
        title=data.title,
        description=data.description,
        priority=data.priority,
        due_date=data.due_date,
        completed=False,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    return db.get(models.Task, task_id)

def update_task(db: Session, task: models.Task, data: schemas.TaskUpdate) -> models.Task:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: models.Task) -> None:
    db.delete(task)
    db.commit()

def list_tasks(
    db: Session,
    completed: Optional[bool],
    priority: Optional[int],
    q: Optional[str],
    page: int,
    page_size: int,
) -> Tuple[Sequence[models.Task], int]:
    stmt = select(models.Task)
    conds = []

    if completed is not None:
        conds.append(models.Task.completed == completed)
    if priority is not None:
        conds.append(models.Task.priority == priority)
    if q:
        like = f"%{q}%"
        conds.append(or_(models.Task.title.ilike(like), models.Task.description.ilike(like)))

    if conds:
        stmt = stmt.where(and_(*conds))

    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    stmt = stmt.order_by(models.Task.due_date.is_(None), models.Task.due_date.asc().nulls_last(), models.Task.priority.asc(), models.Task.id.asc())
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    rows = db.execute(stmt).scalars().all()
    return rows, int(total or 0)

