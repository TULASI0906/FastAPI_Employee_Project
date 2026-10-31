
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from . import models
from .database import Base, engine, get_db
from .schemas import Priority, WorkItemCreate, WorkItemResponse, WorkStatus
from .services import create_work_item, get_work_item, get_work_items


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Work Item Service", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "work_item_service"}


@app.post("/work-items", response_model=WorkItemResponse, status_code=201)
def add_work_item(data: WorkItemCreate, db: Session = Depends(get_db)):
    return create_work_item(db, data)


@app.get("/work-items", response_model=list[WorkItemResponse])
def list_work_items(
    search: Optional[str] = None,
    status: Optional[WorkStatus] = None,
    priority: Optional[Priority] = None,
    employee_id: Optional[int] = Query(default=None, gt=0),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return get_work_items(
        db,
        search=search,
        status=status.value if status else None,
        priority=priority.value if priority else None,
        employee_id=employee_id,
        skip=skip,
        limit=limit,
    )


@app.get("/work-items/{work_item_id}", response_model=WorkItemResponse)
def work_item_details(work_item_id: int, db: Session = Depends(get_db)):
    if work_item_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="Work item ID must be positive",
        )

    return get_work_item(db, work_item_id)
