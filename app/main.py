from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Path
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app import models
from app.schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee,
    update_employee,
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
    response_model=list[EmployeeResponse]
)
def get_employees(
    db: Session = Depends(get_db)
):
    return get_all_employees(db)


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