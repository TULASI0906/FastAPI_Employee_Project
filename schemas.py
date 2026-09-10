from enum import Enum
from pydantic import BaseModel, EmailStr, Field
class WorkMode(str, Enum):
    WFH = "WFH"
    WFO = "WFO"
class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    department: str = Field(min_length=1)
    primary_skill: str = Field(min_length=1)
    location: str = Field(min_length=1)
    work_mode: WorkMode

class EmployeeUpdate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    department: str = Field(min_length=1)
    primary_skill: str = Field(min_length=1)
    location: str = Field(min_length=1)
    work_mode: WorkMode
    is_active: bool

class EmployeeResponse(BaseModel):
     id: int
     name: str
     email: EmailStr
     department: str
     primary_skill: str
     location: str
     work_mode: WorkMode
     is_active: bool
     created_at: str