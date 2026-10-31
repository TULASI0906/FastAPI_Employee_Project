
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models
from .database import Base, engine, get_db
from .schemas import EmployeeCreate, EmployeeResponse
from .services import create_employee, get_employee, get_employees


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Employee Service", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "employee_service"}


@app.post("/employees", response_model=EmployeeResponse, status_code=201)
def add_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee(db, data)


@app.get("/employees", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    return get_employees(db)


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def employee_details(employee_id: int, db: Session = Depends(get_db)):
    if employee_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="Employee ID must be positive",
        )

    return get_employee(db, employee_id)
