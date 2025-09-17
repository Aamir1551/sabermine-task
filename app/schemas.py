from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, constr, conint

TitleStr = constr(strip_whitespace=True, min_length=1, max_length=255)
DescStr = constr(strip_whitespace=True, min_length=0, max_length=2000)

class TaskBase(BaseModel):
    title: TitleStr
    description: Optional[DescStr] = None
    priority: conint(ge=1, le=3) = Field(..., description="1=High, 2=Medium, 3=Low")
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[TitleStr] = None
    description: Optional[DescStr] = None
    priority: Optional[conint(ge=1, le=3)] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None

class TaskOut(TaskBase):
    id: int
    completed: bool = False

    class Config:
        from_attributes = True

