from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException

from app.models import Employee, WorkItem
from app.schemas import EmployeeCreate, EmployeeUpdate, WorkItemCreate


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

        if search:
            search = search.strip()

            if search:
                query = query.filter(
                    func.lower(Employee.name).contains(search.lower())
                )

        if department:
            query = query.filter(
                Employee.department == department
            )

        if work_mode:
            query = query.filter(
                Employee.work_mode == work_mode
            )

        if is_active is not None:
            query = query.filter(
                Employee.is_active == is_active
            )

        total = query.count()

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


def create_work_item(db: Session, data: WorkItemCreate):
    employee = (
        db.query(Employee)
        .filter(Employee.id == data.employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    work_item = WorkItem(
        title=data.title.strip(),
        description=data.description,
        employee_id=data.employee_id,
        status=data.status.value,
        priority=data.priority.value,
        due_date=data.due_date,
        created_at=datetime.now()
    )

    try:
        db.add(work_item)
        db.commit()
        db.refresh(work_item)

        return work_item

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while creating work item"
        )


def get_work_items(
    db,
    search=None,
    employee_id=None,
    status=None,
    priority=None,
    limit=10,
    offset=0
):
    query = db.query(WorkItem)

    if search:
        query = query.filter(
            WorkItem.title.ilike(f"%{search}%")
        )

    if employee_id is not None:
        query = query.filter(
            WorkItem.employee_id == employee_id
        )

    if status is not None:
        query = query.filter(
            WorkItem.status == status.value
        )

    if priority is not None:
        query = query.filter(
            WorkItem.priority == priority.value
        )

    total = query.count()

    items = (
        query
        .order_by(WorkItem.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }

def get_work_item(db, work_item_id):
    work_item = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )

    if work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )

    return work_item


def update_work_item(db, work_item_id, data):
    work_item = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )

    if work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )

    if data.title is not None:
        work_item.title = data.title.strip()

    if data.description is not None:
        work_item.description = data.description

    if data.employee_id is not None:
        employee = (
            db.query(Employee)
            .filter(Employee.id == data.employee_id)
            .first()
        )

        if employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        work_item.employee_id = data.employee_id

    if data.status is not None:
        work_item.status = data.status.value

    if data.priority is not None:
        work_item.priority = data.priority.value

    if data.due_date is not None:
        work_item.due_date = data.due_date

    try:
        db.commit()
        db.refresh(work_item)

        return work_item

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while updating work item"
        )


def delete_work_item(db, work_item_id):
    work_item = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )

    if work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )

    db.delete(work_item)
    db.commit()

    return None