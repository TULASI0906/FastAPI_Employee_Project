from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException

from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate


def create_employee(db: Session, data: EmployeeCreate):
    try:
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

        db.add(employee)
        db.commit()
        db.refresh(employee)

        return employee

    except HTTPException:
        raise

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Employee with this email already exists"
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while creating employee"
        )


def get_all_employees(db: Session):
    try:
        return db.query(Employee).all()

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while fetching employees"
        )


def get_employee(db: Session, employee_id: int):
    try:
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

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while fetching employee"
        )


def update_employee(
    db: Session,
    employee_id: int,
    data: EmployeeUpdate
):
    try:
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

        db.commit()
        db.refresh(employee)

        return employee

    except HTTPException:
        raise

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while updating employee"
        )


def delete_employee(db: Session, employee_id: int):
    try:
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

        db.delete(employee)
        db.commit()

        return {"message": "Employee deleted successfully"}

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while deleting employee"
        )