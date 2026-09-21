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


def get_all_employees(
    db: Session,
    search: str | None = None,
    department: str | None = None,
    work_mode: str | None = None,
    is_active: bool | None = None,
    limit: int = 10,
    offset: int = 0
):
    try:
        query = db.query(Employee)

        # Search by employee name
        if search:
            search = search.strip()

            if search:
                query = query.filter(
                    func.lower(Employee.name).contains(search.lower())
                )

        # Department filter
        if department:
            query = query.filter(
                Employee.department == department
            )

        # Work mode filter
        if work_mode:
            query = query.filter(
                Employee.work_mode == work_mode
            )

        # Active/inactive filter
        if is_active is not None:
            query = query.filter(
                Employee.is_active == is_active
            )

        # Count matching records BEFORE pagination
        total = query.count()

        # Sort by employee ID ascending
        employees = (
            query
            .order_by(Employee.id.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "items": employees
        }

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

        return {
            "message": "Employee deleted successfully"
        }

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while deleting employee"
        )