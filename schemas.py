from enum import Enum
from pydantic import BaseModel, EmailStr
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

class EmployeeUpdate(BaseModel):
     name: str
     email: EmailStr
     department: str
     primary_skill: str
     location: str
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