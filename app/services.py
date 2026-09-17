from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate


def create_employee(db: Session, data: EmployeeCreate):
    email = str(data.email).lower()

    existing = (
        db.query(Employee)
        .filter(func.lower(Employee.email) == email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Employee with this email already exists"
        )

    employee = Employee(
        name=data.name,
        email=email,
        department=data.department,
        primary_skill=data.primary_skill,
        location=data.location,
        work_mode=data.work_mode.value,
        is_active=True
    )

    try:
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Employee with this email already exists"
        )


def get_all_employees(db: Session):
    return db.query(Employee).all()


def get_employee(db: Session, employee_id: int):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


def update_employee(
    db: Session,
    employee_id: int,
    data: EmployeeUpdate
):
    employee = get_employee(db, employee_id)

    email = str(data.email).lower()

    existing = (
        db.query(Employee)
        .filter(
            func.lower(Employee.email) == email,
            Employee.id != employee_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    employee.name = data.name
    employee.email = email
    employee.department = data.department
    employee.primary_skill = data.primary_skill
    employee.location = data.location
    employee.work_mode = data.work_mode.value
    employee.is_active = data.is_active

    try:
        db.commit()
        db.refresh(employee)
        return employee

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


def delete_employee(db: Session, employee_id: int):
    employee = get_employee(db, employee_id)

    try:
        db.delete(employee)
        db.commit()

        return {
            "message": "Employee deleted successfully"
        }

    except Exception:
        db.rollback()
        raise