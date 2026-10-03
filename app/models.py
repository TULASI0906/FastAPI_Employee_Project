from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    __table_args__ = (
        UniqueConstraint("email", name="uq_employee_email"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(225),
        nullable=False,
        unique=True
    )

    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    primary_skill: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    work_mode: Mapped[str] = mapped_column(
        String(3),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )
    work_items = relationship("WorkItem", back_populates="employee")


class WorkItem(Base):
    __tablename__="work_items"
    id= Column(Integer,primary_key=True,autoincrement=True)
    title=Column(String(100),nullable=False)
    description=Column(Text,nullable=True)
    employee_id=Column(Integer,ForeignKey("employees.id"),nullable=False,index=True)
    status=Column(String(20),nullable=False,default="TODO")
    priority=Column(String(20),nullable=False,default="MEDIUM")
    due_date=Column(Date,nullable=True)
    created_at=Column(DateTime, default=datetime.now, nullable=False)
    employee = relationship("Employee", back_populates="work_items")

