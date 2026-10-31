
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    department: str = Field(min_length=1, max_length=100)
    primary_skill: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=100)
    work_mode: str

    @field_validator(
        "name", "department", "primary_skill", "location", mode="before"
    )
    @classmethod
    def validate_required_text(cls, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Field cannot be blank")
        return value.strip()

    @field_validator("work_mode", mode="before")
    @classmethod
    def validate_work_mode(cls, value):
        if not isinstance(value, str) or value.strip().upper() not in {"WFH", "WFO"}:
            raise ValueError("work_mode must be WFH or WFO")
        return value.strip().upper()


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: str
    is_active: bool
    created_at: datetime
