
import os

import httpx
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .models import WorkItem
from .schemas import WorkItemCreate


def verify_employee(employee_id: int):
    base_url = os.getenv("EMPLOYEE_SERVICE_URL", "").rstrip("/")

    if not base_url:
        raise HTTPException(
            status_code=503,
            detail="Employee Service URL is not configured",
        )

    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(
                f"{base_url}/employees/{employee_id}"
            )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Employee not found",
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=503,
                detail="Employee Service returned an unexpected response",
            )

    except HTTPException:
        raise

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=503,
            detail="Employee Service request timed out",
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Employee Service is unavailable",
        )


def create_work_item(db: Session, data: WorkItemCreate):
    if data.status != "TODO" and data.status.value != "TODO":
        raise HTTPException(
            status_code=400,
            detail="New work items must have status TODO",
        )

    verify_employee(data.employee_id)

    item_data = data.model_dump(exclude={"status", "priority"})
    item_data["status"] = data.status.value
    item_data["priority"] = data.priority.value

    work_item = WorkItem(**item_data)

    try:
        db.add(work_item)
        db.commit()
        db.refresh(work_item)
        return work_item

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save work item",
        )


def get_work_items(
    db: Session,
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    employee_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
):
    query = db.query(WorkItem)

    if search:
        query = query.filter(
            WorkItem.title.ilike(f"%{search}%")
        )

    if status:
        query = query.filter(WorkItem.status == status)

    if priority:
        query = query.filter(WorkItem.priority == priority)

    if employee_id is not None:
        query = query.filter(WorkItem.employee_id == employee_id)

    return (
        query.order_by(WorkItem.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_work_item(db: Session, work_item_id: int):
    item = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found",
        )

    return item
