from datetime import datetime
from fastapi import FastAPI, HTTPException, Path
from schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse
app = FastAPI(title="Employee Management API")
@app.get("/health")
def health():
    return {"status": "healthy"}

    
employees = [
    {
        "id": 1,
        "name": "Tulasi",
        "email": "tulasi@gmail.com",
        "department": "IT",
        "primary_skill": "Python",
        "location": "Hyderabad",
        "work_mode": "WFO",
        "is_active": True,
        "created_at": datetime.now().astimezone().isoformat()
    },
    {
        "id": 2,
        "name": "Veera",
        "email": "veera@gmail.com",
        "department": "HR",
        "primary_skill": "Recruitment",
        "location": "Hyderabad",
        "work_mode": "WFH",
        "is_active": True,
        "created_at": datetime.now().astimezone().isoformat()
    },
    {
        "id": 3,
        "name": "Pramodh",
        "email": "pramodh@gmail.com",
        "department": "Finance",
        "primary_skill": "Excel",
        "location": "Bangalore",
        "work_mode": "WFO",
        "is_active": True,
        "created_at": datetime.now().astimezone().isoformat()
    },
    {
        "id": 4,
        "name": "Pranay",
        "email": "pranay@gmail.com",
        "department": "Marketing",
        "primary_skill": "Digital Marketing",
        "location": "Chennai",
        "work_mode": "WFH",
        "is_active": True,
        "created_at": datetime.now().astimezone().isoformat()
    },
    {
        "id": 5,
        "name": "Hemanth",
        "email": "hemanth@gmail.com",
        "department": "IT",
        "primary_skill": "Java",
        "location": "Pune",
        "work_mode": "WFO",
        "is_active": True,
        "created_at": datetime.now().astimezone().isoformat()
    }
]

next_id = 6


@app.post("/employees", status_code=201)
def create_employee(data: EmployeeCreate):
    global next_id
    for employee in employees:
        if employee["email"].lower() == data.email.lower():
            raise HTTPException(status_code=400, detail="Employee with this email already exists")
        
    new_employee = {
        "id": next_id,
        "name": data.name,
        "email": data.email,
        "department": data.department,
        "primary_skill": data.primary_skill,
        "location": data.location,
        "work_mode": data.work_mode.value,     
        "is_active": True,
        "created_at": datetime.now().astimezone().isoformat()
    }
    employees.append(new_employee)
    next_id += 1 
    return new_employee


@app.get("/employees")
def get_employees():
    return employees

@app.get("/employees/{id}")
def get_employee(id: int = Path(gt=0)):
    for employee in employees:
        if employee["id"] == id:
            return employee
    raise HTTPException(status_code=404, detail="Employee not found")

@app.put("/employees/{id}")
def put_employee(data: EmployeeUpdate, id: int = Path(gt=0)):
    employee = None

    for emp in employees:
        if emp["id"] == id:
            employee = emp
            break

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    for other in employees:
        if other["id"] != id and other["email"].lower() == data.email.lower():
            raise HTTPException(status_code=400, detail="Email already exists")

    employee["name"] = data.name
    employee["email"] = data.email
    employee["department"] = data.department
    employee["primary_skill"] = data.primary_skill
    employee["location"] = data.location
    employee["work_mode"] = data.work_mode.value
    employee["is_active"] = data.is_active

    return employee


@app.delete("/employees/{id}")
def delete_employee(id: int = Path(gt=0)):
    for employee in employees:
        if employee["id"] == id:
            employees.remove(employee)
            return {"message": "Employee deleted successfully"}
    raise HTTPException(status_code=404, detail="Employee not found")