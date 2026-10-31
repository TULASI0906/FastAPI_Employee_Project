
from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Integer, String, Text

from .database import Base


class WorkItem(Base):
    __tablename__ = "work_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    employee_id = Column(Integer, nullable=False, index=True)
    status = Column(String(20), nullable=False, default="TODO")
    priority = Column(String(10), nullable=False, default="MEDIUM")
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
