from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class WorkMode(str, Enum):
    WFH = "WFH"
    WFO = "WFO"


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: WorkMode

    @field_validator("name", "department", "primary_skill", "location")
    @classmethod
    def validate_required_fields(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty or whitespace-only")

        return value


class EmployeeUpdate(BaseModel):
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: WorkMode
    is_active: bool

    @field_validator("name", "department", "primary_skill", "location")
    @classmethod
    def validate_required_fields(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty or whitespace-only")

        return value


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: WorkMode
    is_active: bool
    created_at: datetime
