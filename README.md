# Employee Management API

## Project Overview

This project is a FastAPI backend application used to manage employee records.

In Task 2, the application was connected to a MySQL database using SQLAlchemy. Employee records are stored in MySQL instead of a temporary Python list, so the data remains available even after restarting the application.

The project provides APIs to create, view, update, and delete employee records. It also includes validation, search, filtering, pagination, database error handling, and work item management.

## Technologies Used

- Python 3.12
- FastAPI
- Pydantic
- MySQL
- SQLAlchemy
- PyMySQL
- python-dotenv
- Uvicorn
- Swagger UI
- Git

## Project Structure

```text
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
Features
Create, view, update, and delete employee records
Store employee data in MySQL
Validate employee details
Validate email format
Prevent duplicate email addresses
Perform case-insensitive email uniqueness checks
Validate work mode
Validate employee IDs
Search employees
Filter employees
Pagination using limit and offset
Create and manage work items
Assign work items to employees
Search and filter work items
Update and reassign work items
Delete work items
Validate work item status and priority
Handle database errors using rollback
Verify database persistence after application restart
Task 2 - MySQL Database Integration
Database Setup

MySQL is used as the database for this project.

The database was created using MySQL Workbench:

CREATE DATABASE employee_db;
USE employee_db;

The application uses an employees table to store employee information.

SQLAlchemy is used to define the database models and communicate with MySQL.

Environment Configuration

The database connection details are stored in a local .env file.

Example:

DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/employee_db

The actual .env file contains the local database password and is not committed to Git.

Setup and Installation
1. Create a virtual environment
py -3.12 -m venv venv
2. Activate the virtual environment
venv\Scripts\activate
3. Install the required packages
pip install -r requirements.txt
4. Start MySQL

Make sure the MySQL server is running before starting the FastAPI application.

5. Run the FastAPI application
uvicorn app.main:app --reload
6. Open Swagger UI
http://127.0.0.1:8000/docs

Employee Fields
Field	            Description
id	                Automatically generated employee ID
name	            Employee name
email	            Employee email address
department	        Employee department
primary_skill	    Primary skill of the employee
location	        Employee location
work_mode	        Either WFH or WFO
is_active	        Employee active status
created_at	        Automatically generated creation date and time

Employee API Endpoints
Method	        Endpoint	        Description
GET	            /health	            Check application health
POST	        /employees	        Create a new employee
GET	            /employees	        Get all employees
GET	            /employees/{id}	    Get an employee by ID
PUT	            /employees/{id}	    Update employee details
DELETE	        /employees/{id}	    Delete an employee

Employee Validation

The following validations are implemented:

Employee name is required.
Department is required.
Primary skill is required.
Location is required.
Required fields cannot contain only spaces.
Email must have a valid email format.
Email addresses must be unique.
Email uniqueness is checked without considering letter case.
Work mode must be either WFH or WFO.
Employee ID must be greater than 0.
A missing employee returns 404 Not Found.
A duplicate email returns an appropriate error response.
A successful employee creation returns 201 Created.
Database Error Handling

Database operations are handled using SQLAlchemy sessions.

When a database operation fails, the transaction is rolled back so that the failed change does not remain in the database.

The database session is also properly closed after the request.

Database Persistence

Employee records are stored in MySQL instead of a Python list.

An employee was created and stored in the database. After restarting the FastAPI application, the employee was still available.

This confirmed that the employee data is persisted in MySQL.

Task 3 - Search, Filtering and Pagination
Overview

Task 3 extends the employee API by adding search, filtering, and pagination to the GET /employees endpoint.

Query Parameters

Parameter	            Description
search	                Searches employee names using partial, case-insensitive matching
department	            Filters employees by department
work_mode	            Filters employees by WFH or WFO
is_active	            Filters employees by active status
limit	                Number of records to return. Default is 10, maximum is 100
offset	                Number of matching records to skip. Default is 0

The filters can be used individually or together.

Example Requests
GET /employees?search=tula
GET /employees?department=Engineering
GET /employees?work_mode=WFH
GET /employees?is_active=true
GET /employees?limit=5&offset=0
GET /employees?limit=5&offset=5
GET /employees?department=Engineering&work_mode=WFH&limit=5&offset=0

Response Format

The response contains the total number of matching records, along with the requested limit, offset, and employee records.

{
  "total": 10,
  "limit": 5,
  "offset": 0,
  "items": []
}

The total is calculated before applying limit and offset.

Employees are returned in ascending order of employee ID.

If there are no matching employees, the API returns 200 OK with an empty items list.

Pagination
limit controls how many records are returned.
offset controls how many matching records are skipped.

For example:

limit=5&offset=0

returns the first five matching records.

limit=5&offset=5

skips the first five records and returns the next set.



Task 3 Validation

The following validations were implemented:

limit must be at least 1.
limit cannot be greater than 100.
offset cannot be negative.
Work mode must be a valid value.
Search and filters can be combined.
SQLAlchemy is used for database filtering, counting, ordering, and pagination.


Task 4 - Work Item Management
Task 4 Overview

Task 4 extends the Employee Management API by adding work item management.

A new work_items table was added to the MySQL database.

Each work item is assigned to an existing employee using employee_id.

The work_items table is connected to the employees table using a foreign key and SQLAlchemy relationship.

The new APIs allow work items to be created, viewed, searched, filtered, updated, reassigned, and deleted.

Database Relationship

There are two related tables:

Employees Table

The employees table stores employee information.

The main identifier is:

employees.id

This is the primary key of the employees table.

Work Items Table

The work_items table stores work assigned to employees.

The main identifiers are:

work_items.id
work_items.employee_id

work_items.id is the primary key of the work items table.

work_items.employee_id is the foreign key.

The relationship is:

employees.id
     ↑
     |
work_items.employee_id

In simple terms, the employee_id in the work items table stores the ID of the employee to whom the work item is assigned.

One employee can have multiple work items, so this is a one-to-many relationship.

Primary Key and Foreign Key

A primary key uniquely identifies a record in its own table.

For example:

employees.id
work_items.id

are primary keys.

A foreign key connects one table to another table.

For example:

work_items.employee_id

references:

employees.id

The foreign key was verified in MySQL using:

SHOW CREATE TABLE work_items;

The table definition contains:

FOREIGN KEY (employee_id) REFERENCES employees(id)

This means a work item's employee_id refers to an existing employee's id.

Work Item Fields

Field	        Description
id	            Automatically generated work item ID and primary key
title	        Required work item title
description	    Optional description
employee_id	    Assigned employee ID and foreign key
status	        TODO, IN_PROGRESS, or COMPLETED
priority	    LOW, MEDIUM, or HIGH
due_date	    Optional due date
created_at	    Automatically generated date and time

Default values:

status   → TODO
priority → MEDIUM

Task 4 API Endpoints
POST /work-items

Creates a new work item and assigns it to an existing employee.

A successful request returns:

201 Created

Example request:

{
  "title": "Prepare weekly report",
  "description": "Prepare and send the weekly report",
  "employee_id": 3,
  "status": "TODO",
  "priority": "MEDIUM",
  "due_date": "2026-10-05"
}

If the employee does not exist, the API returns:

404 Not Found
GET /work-items

Returns work items with optional search, filtering, and pagination.

Supported query parameters:

Parameter	        Description
search	            Partial, case-insensitive search by title
employee_id	        Filter by assigned employee
status	            Filter by work item status
priority	        Filter by priority
limit	            Number of records to return
offset	            Number of records to skip

All supplied filters are applied together.

Example:

GET /work-items?search=weekly&employee_id=3&status=TODO&priority=MEDIUM&limit=10&offset=0

The response format is:

{
  "total": 2,
  "limit": 10,
  "offset": 0,
  "items": []
}

The total represents the number of matching records before pagination is applied.

Work items are returned in ascending order of ID.

GET /work-items/{work_item_id}

Returns a specific work item using its ID.

Example:

GET /work-items/1

If the work item does not exist, the API returns:

404 Not Found
PUT /work-items/{work_item_id}

Updates an existing work item.

The work item can also be reassigned to another employee.

For example, the employee assigned to the work item can be changed from one employee ID to another existing employee ID.

If the new employee does not exist, the API returns:

404 Not Found
DELETE /work-items/{work_item_id}

Deletes a work item.

A successful deletion returns:

204 No Content

After deletion, trying to get the same work item returns:

404 Not Found
Work Item Validation

The following validation rules are implemented:

title is required.
Title cannot be blank or contain only spaces.
employee_id must be greater than 0.
The assigned employee must exist.
Status must be one of:
TODO
IN_PROGRESS
COMPLETED
Priority must be one of:
LOW
MEDIUM
HIGH
limit must be between 1 and 100.
offset cannot be negative.
A missing work item returns 404 Not Found.
A missing employee returns 404 Not Found.
Invalid status or priority returns 422 Unprocessable Entity.
Blank title returns 422 Unprocessable Entity.
Assigned Employee Response

Every work item response includes the employee assigned to that work item.

For example:

{
  "id": 1,
  "title": "Updated weekly report",
  "description": "Prepare and send the weekly report",
  "employee_id": 4,
  "status": "IN_PROGRESS",
  "priority": "HIGH",
  "due_date": "2026-10-06",
  "created_at": "2026-10-03T...",
  "assigned_employee": {
    "id": 4,
    "name": "Tulasi",
    "email": "example@email.com",
    "department": "...",
    "primary_skill": "...",
    "location": "...",
    "work_mode": "WFO"
  }
}

The assigned_employee information comes from the SQLAlchemy relationship between WorkItem and Employee.

Task 4 Testing

The Task 4 APIs were tested using Swagger UI.

The following test cases were completed:

Create a work item for an existing employee.
Create a work item with a nonexistent employee.
Get a work item by ID.
Search work items by title.
Filter work items by employee ID.
Filter work items by status.
Filter work items by priority.
Combine multiple filters.
Test pagination using limit and offset.
Update a work item.
Reassign a work item to another employee.
Test invalid status.
Test invalid priority.
Test blank title.
Get a missing work item.
Delete a work item.
Verify the deleted work item returns 404.
Restart the application and verify persistence.
Verify that existing employee APIs still work.
MySQL Verification

The database structure was checked using MySQL Workbench.

The following commands were used:

SHOW TABLES;

This was used to check which tables exist in the database.

DESCRIBE work_items;

This was used to check the columns, data types, keys, and nullable values of the work_items table.

SHOW CREATE TABLE work_items;

This was used to see the complete SQL definition of the existing work_items table.

It also helped verify the foreign key relationship.

The foreign key was confirmed as:

FOREIGN KEY (employee_id) REFERENCES employees(id)
Work Items Table Structure

The work_items table contains:

id
title
description
employee_id
status
priority
due_date
created_at

The employee_id column is connected to the employees.id column.

Database Persistence Test

A work item was created and stored in MySQL.

The FastAPI application was then restarted.

After restarting the application, the work item was still available through the API.

This confirmed that the work item data is stored persistently in MySQL.

What I Learned

Through these tasks, I learned how to:

Build a FastAPI backend.
Create REST APIs.
Connect FastAPI with MySQL.
Use SQLAlchemy for database operations.
Create database models.
Use Pydantic schemas for validation.
Separate routes, schemas, models, and services.
Manage database sessions.
Handle database errors using rollback.
Implement CRUD operations.
Implement search and filtering.
Implement pagination using limit and offset.
Understand primary keys and foreign keys.
Create relationships between database tables.
Use SQLAlchemy relationships.
Assign work items to existing employees.
Update and reassign work items.
Validate enum values.
Test APIs using Swagger UI.
Verify database tables using MySQL Workbench.
Verify foreign key relationships.
Check persistence after restarting the application.
Use Git for version control.
Difficulties Faced

Initially, I found SQLAlchemy and database sessions difficult to understand.

I also needed some time to understand how the different project files work together.

The main files have different responsibilities:

models.py
→ Represents the database table structure.

schemas.py
→ Defines the API request and response structure and validation.

services.py
→ Contains the main database and business logic.

main.py
→ Defines the FastAPI routes and endpoints.

database.py
→ Handles the database connection and session.

In Task 4, understanding the difference between a primary key, foreign key, and SQLAlchemy relationship was initially difficult.

Testing the APIs through Swagger UI and checking the actual database tables in MySQL Workbench helped me understand how the application works from API request to database and back to the API response.

Assumptions:
An employee must already exist before a work item can be assigned to that employee.
Status values are restricted to TODO, IN_PROGRESS, and COMPLETED.
Priority values are restricted to LOW, MEDIUM, and HIGH.
Employee IDs and work item IDs must be positive integers.
MySQL is running locally during development.
Database connection details are stored in the local .env file.
The .env file is not committed to Git.
Authentication is not implemented because it is not required for this task.
Frontend is not implemented because this is a backend project.
Docker is not implemented because it is not required for this task.
Database migrations are not implemented because they are not required for this task.
Screenshots

The screenshots folder contains screenshots of the API testing and database verification.

The screenshots include:

Work item creation request and response
Nonexistent employee request and response
Get work item by ID
Get all work items
Search results
Employee filter
Status filter
Priority filter
Combined filters
Pagination
Missing work item
Update and reassignment
Invalid status
Invalid priority
Blank title
Delete response
Delete verification
Persistence after application restart
Existing employee API
MySQL DESCRIBE work_items
MySQL foreign key verification
Git and Submission

The completed Task 4 work is maintained in the task-4 branch.

Before pushing the project, make sure the following files are not committed:

.env
venv/
.venv/
__pycache__/

The final project should be pushed to the task-4 branch along with the README and screenshots.

Conclusion

The Employee Management API was extended from basic employee CRUD operations to a database-backed application with search, filtering, pagination, and work item management.

Task 4 adds a work_items table and connects it with the existing employees table using a foreign key and SQLAlchemy relationship.

The APIs were tested through Swagger UI, and the database structure and foreign key relationship were verified using MySQL Workbench.

The project now supports both employee management and work item management with validation, filtering, pagination, database persistence, and related employee information in work item responses.