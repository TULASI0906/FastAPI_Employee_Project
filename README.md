# Employee Management API

## Project Overview

This project is a FastAPI application used to manage employees and their work items.

The project was completed in different tasks:

- Task 1 - Created employee APIs using a Python list.
- Task 2 - Connected the application to MySQL using SQLAlchemy.
- Task 3 - Added search, filters and pagination for employees.
- Task 4 - Added work item management and connected work items to employees.

Employee and work item data is stored in MySQL, so the data remains available even after restarting the application.

## Technologies Used

- Python 3.12
- FastAPI
- Pydantic
- MySQL
- SQLAlchemy
- PyMySQL
- Uvicorn
- Swagger UI
- Git

## Project Structure

FastAPI_Employee_Project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
├── screenshots/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

Task 2 - Employee Management
In Task 2, the employee application was connected to a MySQL database.
Employee details are stored in the database instead of a temporary Python list.
Employee APIs
Method	Endpoint	Purpose
GET	/health	Check application health
POST	/employees	Create employee
GET	/employees	Get all employees
GET	/employees/{id}	Get employee by ID
PUT	/employees/{id}	Update employee
DELETE	/employees/{id}	Delete employee


Employee Details
An employee contains:
- ID
- Name
- Email
- Department
- Primary Skill
- Location
- Work Mode
- Active Status
- Created Date

Employee Validation
- Name, department, skill and location are required.
- Empty or blank values are not allowed.
- Email must be valid.
- Email must be unique.
- Email uniqueness is checked without considering capital or small letters.
- Work mode can be WFH or WFO.
- Employee ID must be greater than 0.
- A new employee returns 201 Created.
- A duplicate email returns 400 Bad Request.
- A missing employee returns 404 Not Found.

Database Setup
Create the database in MySQL Workbench:
CREATE DATABASE employee_db;

Then:
USE employee_db;

The database connection is stored in the .env file.
Example:
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/employee_db

The real password is kept only in the local .env file.

How to Run the Project
Create virtual environment:
py -3.12 -m venv venv

Activate it:
venv\Scripts\activate

Install packages:
pip install -r requirements.txt

Run the application:
uvicorn app.main:app --reload

Open Swagger:
http://127.0.0.1:8000/docs

Task 2 Testing
The employee APIs were tested using Swagger UI.
The following were tested:
- Create employee
- Get all employees
- Get employee by ID
- Update employee
- Delete employee
- Duplicate email
- Case-insensitive duplicate email
- Blank fields
- Non-existing employee
- Database persistence after restarting the application


Task 3 - Search, Filtering and Pagination
Task 3 added search, filters and pagination to:
GET /employees

Search
Search employees by name.
Example:
GET /employees?search=tula

The search supports partial names and is not affected by capital or small letters.
Filters
Filter by department:
GET /employees?department=Engineering

Filter by work mode:
GET /employees?work_mode=WFH

Filter by active status:
GET /employees?is_active=true

Pagination
Pagination uses limit and offset.
Example:
GET /employees?limit=5&offset=0

GET /employees?limit=5&offset=5

- limit tells how many records to return.
- offset tells how many records to skip.
Default limit is 10.
Limit can be from 1 to 100.
Negative offset is not allowed.
Multiple Filters
Different filters can be used together.
Example:
GET /employees?department=Engineering&work_mode=WFH&limit=5&offset=0

Task 3 Testing
The following were tested using Swagger:
- Employee name search
- Department filter
- Work mode filter
- Active status filter
- Multiple filters together
- Pagination
- Offset 0
- Offset 5
- Offset greater than available records
- No matching employees
- Invalid limit
- Negative offset
- Invalid work mode

Task 3 - What I Learned
- How search works in an API.
- How to use filters.
- How limit and offset work.
- How to use multiple filters together.
- How to test query parameters in Swagger.

Task 3 - Difficulties Faced
Initially, I found it difficult to understand how search, filters and pagination work together.
Testing different combinations in Swagger helped me understand them better.

Task 4 - Work Item Management
Task 4 adds work items to the Employee Management API.
A work item is assigned to an employee.
Work items are stored in a separate work_items table in MySQL.
Work Item Details
A work item contains:
- ID
- Title
- Description
- Employee ID
- Status
- Priority
- Due Date
- Created Date
Work Item Status
A work item can have:
- TODO
- IN_PROGRESS
- COMPLETED
Work Item Priority
A work item can have:
- LOW
- MEDIUM
- HIGH
Database Relationship
Each work item belongs to an employee.
The employee_id in the work item points to the employee ID.
Simple example:
Employee 1
    ↓
Work Item 1
Work Item 2

This means Employee 1 has two work items.
A work item can only be created for an employee who already exists.
If an employee has work items assigned, the employee cannot be deleted.
The work items must first be reassigned or deleted.
Task 4 - Work Item APIs
Create Work Item
POST /work-items

Example:
{
  "title": "Prepare weekly report",
  "description": "Prepare the weekly report",
  "employee_id": 1,
  "status": "TODO",
  "priority": "MEDIUM",
  "due_date": "2026-10-10"
}

Successful creation returns:
201 Created

Get Work Items
GET /work-items

It supports:
- Search by title
- Employee filter
- Status filter
- Priority filter
- Limit
- Offset
Example:
GET /work-items?employee_id=1&status=TODO&limit=5&offset=0

Get Work Item by ID
GET /work-items/1

This returns the work item with ID 1.
Update Work Item
PUT /work-items/1

Example:
{
  "title": "Updated weekly report",
  "description": "Updated report details",
  "employee_id": 1,
  "status": "IN_PROGRESS",
  "priority": "HIGH",
  "due_date": "2026-10-15"
}

Delete Work Item
DELETE /work-items/1

A successful deletion returns:
204 No Content

Task 4 - Validation and Error Handling
The following cases are handled:
- Title is required.
- Title must have at least 1 character.
- Title cannot be more than 100 characters.
- null title returns 422.
- Employee must exist before assigning a work item.
- Invalid employee returns 404.
- Status must be TODO, IN_PROGRESS or COMPLETED.
- Priority must be LOW, MEDIUM or HIGH.
- Description is optional.
- Sending null for description clears the old description.
- Due date is optional.
- Sending null for due date clears the old date.
- Non-existing work item returns 404.
- Employee with assigned work items cannot be deleted.
- Trying to delete such an employee returns 400.
- The error message tells the user to reassign or delete the work items first.
- Database errors during work item deletion return 500.
- Failed database changes are rolled back.

Task 4 - Database Error and Rollback
When a database error happens while deleting a work item, the application uses rollback.
db.rollback()


The API returns:
500 Internal Server Error

with the message:
Database error while deleting work item

The rollback was tested by causing the error and then checking that the work item still existed.

Task 4 Testing
The following cases were tested using Swagger UI:
- Create work item
- Get work items
- Get work item by ID
- Update work item
- Title null
- Description null
- Due date null
- Employee deletion with assigned work
- Work item deletion database error
- Rollback verification

Task 4 screenshots are available in the Task 4 screenshots folder.
Screenshots:
- Creating work items
- Creating work items with non-existing employees
- Getting a work item by ID
- Getting all work items
- Searching work items
- Filtering by employee
- Filtering by status
- Filtering by priority
- Using combined filters
- Pagination and offset
- Missing work item validation
- Updating and reassigning work items
- Invalid status validation
- Invalid priority validation
- Blank title validation
- Work item deletion
- Delete verification
- Restart persistence
- Existing employee API
- MySQL work_items table structure
- MySQL foreign key relationship
- Null title validation returning 422
- Clearing description and due date using null
- Blocking employee deletion when work items are assigned
- Database error handling during work item deletion
- Rollback verification after database error

Task 4 - Assumptions
- Employee and work item data used for testing is fictional.
- MySQL is running locally.
- Database details are stored in the local .env file.
- A work item can only be assigned to an existing employee.
- An employee cannot be deleted while work items are assigned.
- Authentication and frontend are not included because they are not required for this task.
- Docker and database migrations are not included because they are not required for this task.

Task 4 - What I Learned
Through Task 4, I learned:
- How to create work items.
- How work items are connected to employees.
- How foreign keys are used.
- How to create APIs for work items.
- How to validate work item details.
- How to clear optional fields using null.
- How to prevent deleting an employee who has work items.
- How rollback works when a database error happens.
- How to test APIs using Swagger.

Task 4 - Difficulties Faced
Initially, I had difficulty understanding how work items are connected to employees.
I also found it difficult to understand foreign keys and relationships.
Handling null values during updates was another difficulty.
Understanding rollback and database errors during deletion was also difficult at first.
Testing the APIs in Swagger and checking the database helped me understand these concepts better.