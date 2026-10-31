
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from .models import Employee
from .schemas import EmployeeCreate


def create_employee(db: Session, data: EmployeeCreate):
    existing = (
        db.query(Employee)
        .filter(func.lower(Employee.email) == data.email.lower())
        .first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    employee = Employee(**data.model_dump())

    try:
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not save employee")


def get_employees(db: Session):
    return db.query(Employee).order_by(Employee.id).all()


def get_employee(db: Session, employee_id: int):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee
