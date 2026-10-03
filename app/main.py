from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Path, Query

from sqlalchemy.orm import Session

from app.database import Base, engine, get_db

from app import models

from app.schemas import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
    EmployeeListResponse,
    WorkMode,
    WorkItemCreate,
    WorkItemUpdate,
    WorkItemResponse,
    WorkItemListResponse,
    WorkItemStatus,
    WorkItemPriority
)

from app.services import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee,
    update_employee,
    create_work_item,
    get_work_items,
    get_work_item,
    update_work_item,
    delete_work_item
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Employee Management API",
    lifespan=lifespan
)


@app.get("/health")
def health():
    return {"status": "healthy"}


# ---------------- EMPLOYEE APIs ----------------


@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=201
)
def create_employee_api(
    data: EmployeeCreate,
    db: Session = Depends(get_db)
):
    return create_employee(db, data)


@app.get(
    "/employees",
    response_model=EmployeeListResponse
)
def get_employees(
    search: str | None = Query(
        default=None,
        description="Search employees by name"
    ),
    department: str | None = Query(
        default=None,
        description="Filter by department"
    ),
    work_mode: WorkMode | None = Query(
        default=None,
        description="Filter by WFH or WFO"
    ),
    is_active: bool | None = Query(
        default=None,
        description="Filter by active status"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum records to return"
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of records to skip"
    ),
    db: Session = Depends(get_db)
):
    return get_all_employees(
        db=db,
        search=search,
        department=department,
        work_mode=work_mode,
        is_active=is_active,
        limit=limit,
        offset=offset
    )


@app.get(
    "/employees/{id}",
    response_model=EmployeeResponse
)
def get_employee_by_id(
    id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    return get_employee(db, id)


@app.put(
    "/employees/{id}",
    response_model=EmployeeResponse
)
def update_employee_api(
    data: EmployeeUpdate,
    id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    return update_employee(db, id, data)


@app.delete("/employees/{id}")
def delete_employee_api(
    id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    return delete_employee(db, id)




@app.post(
    "/work-items",
    response_model=WorkItemResponse,
    status_code=201
)
def create_work_item_api(
    data: WorkItemCreate,
    db: Session = Depends(get_db)
):
    return create_work_item(db, data)


@app.get(
    "/work-items",
    response_model=WorkItemListResponse
)
def get_work_items_api(
    search: str | None = None,
    employee_id: int | None = Query(
        default=None,
        gt=0
    ),
    status: WorkItemStatus | None = None,
    priority: WorkItemPriority | None = None,
    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),
    offset: int = Query(
        default=0,
        ge=0
    ),
    db: Session = Depends(get_db)
):
    return get_work_items(
        db,
        search,
        employee_id,
        status,
        priority,
        limit,
        offset
    )


@app.get(
    "/work-items/{work_item_id}",
    response_model=WorkItemResponse
)
def get_work_item_api(
    work_item_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    return get_work_item(db, work_item_id)


@app.put(
    "/work-items/{work_item_id}",
    response_model=WorkItemResponse
)
def update_work_item_api(
    data: WorkItemUpdate,
    work_item_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    return update_work_item(
        db,
        work_item_id,
        data
    )


@app.delete(
    "/work-items/{work_item_id}",
    status_code=204
)
def delete_work_item_api(
    work_item_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    delete_work_item(db, work_item_id)
    return None