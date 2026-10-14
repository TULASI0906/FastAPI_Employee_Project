from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException

from app.models import Employee, WorkItem

from app.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    WorkItemCreate,
    WorkItemStatus
)



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

        assigned_work = (
            db.query(WorkItem)
            .filter(WorkItem.employee_id == employee_id)
            .first()
        )

        if assigned_work is not None:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete employee. Reassign or delete their work items first."
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

    
    if data.status != WorkItemStatus.TODO:
        raise HTTPException(
            status_code=400,
            detail="New work items must start with TODO status"
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



def validate_status_transition(current_status: str, requested_status: str) -> bool:
    if current_status == requested_status:
        return False

    allowed_next_status = {
        "TODO": "IN_PROGRESS",
        "IN_PROGRESS": "COMPLETED"
    }

    if allowed_next_status.get(current_status) != requested_status:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition: {current_status} to {requested_status}"
        )

    return True





def update_work_item(db: Session, work_item_id: int, data):
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

    # Validate status before changing any fields.
    status_changed = False
    if data.status is not None:
        status_changed = validate_status_transition(
            work_item.status,
            data.status.value
        )

    # Validate employee before changing any fields.
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

    try:
        if data.title is not None:
            work_item.title = data.title.strip()

        if "description" in data.model_fields_set:
            work_item.description = data.description

        if data.employee_id is not None:
            work_item.employee_id = data.employee_id

        if status_changed:
            work_item.status = data.status.value

        if data.priority is not None:
            work_item.priority = data.priority.value

        if "due_date" in data.model_fields_set:
            work_item.due_date = data.due_date

        db.commit()
        db.refresh(work_item)
        return work_item

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while updating work item"
        )



def update_work_item_status(db: Session, work_item_id: int, status: WorkItemStatus):
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

    status_changed = validate_status_transition(
        work_item.status,
        status.value
    )

    if not status_changed:
        return work_item

    try:
        work_item.status = status.value
        db.commit()
        db.refresh(work_item)
        return work_item

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while updating work item status"
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

    try:
        db.delete(work_item)
        db.commit()

        return None

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while deleting work item"
        )


def get_employee_work_summary(db: Session, employee_id: int):
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

    counts = (
        db.query(WorkItem.status, func.count(WorkItem.id))
        .filter(WorkItem.employee_id == employee_id)
        .group_by(WorkItem.status)
        .all()
    )

    status_counts = {
        status: count for status, count in counts
    }

    todo = status_counts.get("TODO", 0)
    in_progress = status_counts.get("IN_PROGRESS", 0)
    completed = status_counts.get("COMPLETED", 0)

    return {
        "employee_id": employee_id,
        "total_work_items": todo + in_progress + completed,
        "todo": todo,
        "in_progress": in_progress,
        "completed": completed
    }
