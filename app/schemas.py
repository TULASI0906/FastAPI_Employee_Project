from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class WorkMode(str, Enum):
    WFH = "WFH"
    WFO = "WFO"


class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: WorkMode

    @field_validator(
        "name",
        "department",
        "primary_skill",
        "location"
    )
    @classmethod
    def reject_blank_fields(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty or whitespace-only")

        return value


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    is_active: bool


class EmployeeResponse(EmployeeBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EmployeeListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[EmployeeResponse]

class WorkItemStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class WorkItemPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class AssignedEmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: WorkMode

    model_config = ConfigDict(from_attributes=True)

class WorkItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    employee_id: int = Field(gt=0)
    status: WorkItemStatus = WorkItemStatus.TODO
    priority: WorkItemPriority = WorkItemPriority.MEDIUM
    due_date: date| None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be blank")
        return value




class WorkItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    employee_id: int | None = Field(default=None, gt=0)
    status: WorkItemStatus | None = None
    priority: WorkItemPriority | None = None
    due_date: date | None = None

    @field_validator("title", mode="before")
    @classmethod
    def reject_null_title(cls, value):
        if value is None:
            raise ValueError("Title cannot be null")
        if isinstance(value, str) and not value.strip():
            raise ValueError("Title cannot be blank")
        return value

    @field_validator("employee_id", mode="before")
    @classmethod
    def reject_null_employee_id(cls, value):
        if value is None:
            raise ValueError("Employee ID cannot be null")
        return value

    @field_validator("priority", mode="before")
    @classmethod
    def reject_null_priority(cls, value):
        if value is None:
            raise ValueError("Priority cannot be null")
        return value

    @field_validator("status", mode="before")
    @classmethod
    def reject_null_status(cls, value):
        if value is None:
            raise ValueError("Status cannot be null")
        return value

class WorkItemStatusUpdate(BaseModel):
    status: WorkItemStatus


class WorkItemResponse(BaseModel):
    id: int
    title: str
    description: str | None
    employee_id: int
    status: WorkItemStatus
    priority: WorkItemPriority
    due_date: date | None
    created_at: datetime
    assigned_employee: AssignedEmployeeResponse = Field(validation_alias="employee")

    model_config = ConfigDict(from_attributes=True) 

class WorkItemListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[WorkItemResponse]


class EmployeeWorkSummaryResponse(BaseModel):
    employee_id: int
    total_work_items: int
    todo: int
    in_progress: int
    completed: int
