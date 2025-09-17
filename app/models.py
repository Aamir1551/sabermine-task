from __future__ import annotations
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(String(2000), nullable=True)
    priority = Column(Integer, nullable=False, index=True)  # 1=High,2=Med,3=Low
    due_date = Column(DateTime, nullable=True, index=True)
    completed = Column(Boolean, nullable=False, default=False, index=True)

