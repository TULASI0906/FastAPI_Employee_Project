# Employee Management API

## Project Overview

This project is a FastAPI backend application used to manage employee records.

In Task 2, the application is connected to a MySQL database using SQLAlchemy. Employee records are stored in the database instead of a temporary Python list.

The application provides REST APIs to create, view, update and delete employee information.

Employee records remain available even after restarting the application because the data is stored in MySQL.

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

Features-
Create a new employee
View all employees
View an employee by ID
Update employee details
Delete an employee
Check application health
Validate employee input
Validate email format
Ensure email addresses are unique
Perform case-insensitive email uniqueness checks
Restrict work mode to WFH or WFO
Validate employee ID
Return appropriate HTTP error responses
Store employee records in MySQL
Automatically generate employee IDs
Set is_active to true by default
Automatically generate created_at
Preserve created_at during updates
Handle database errors using rollback
Close database sessions after use

Database Setup-
MySQL is used as the database for this project.

Create Database-
Open MySQL Workbench and run:
CREATE DATABASE employee_db;

Then select the database and run:
USE employee_db;
The application uses an employees table to store employee records.
The table is created through the SQLAlchemy model when the application starts.

Environment Configuration-
Database connection details are stored in a local .env file.

Example:
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/employee_db

The actual .env file contains the local database password and is not committed to Git.

A .env.example file is included with placeholder values for configuration reference.

Setup and Installation-
1. Create a virtual environment
py -3.12 -m venv venv
2. Activate the virtual environment
venv\Scripts\activate
3. Install the required packages
pip install -r requirements.txt
4. Configure the database

Create the .env file and add the MySQL database connection string.

5. Run the FastAPI application
uvicorn app.main:app --reload
6. Open Swagger UI
http://127.0.0.1:8000/docs


API Endpoints-
Method	/Endpoint	       /Description

GET	    /health	           /Check application health
POST	/employees	       /Create a new employee
GET	    /employees	       /Get all employees
GET	    /employees/{id}	   /Get an employee by ID
PUT	    /employees/{id}	   /Update employee details
DELETE	/employees/{id}	   /Delete an employee


Employee Fields-
id - Automatically generated employee ID
name - Employee name
email - Employee email address
department - Employee department
primary_skill - Primary skill of the employee
location - Employee location
work_mode - Either WFH or WFO
is_active - Active status, true by default
created_at - Automatically generated creation timestamp

Validation Rules-
Employee name is required.
Department is required.
Primary skill is required.
Location is required.
Required fields cannot be empty or whitespace-only.
Email must be in a valid email format.
Email addresses must be unique.
Email uniqueness is checked case-insensitively.
Work mode must be either WFH or WFO.
Employee ID must be greater than 0.
A 400 Bad Request response is returned for duplicate emails.
A 404 Not Found response is returned when an employee does not exist.
A 201 Created response is returned after successful employee creation.
Failed database changes are rolled back.

Database Storage-
Employee records are stored in the MySQL employees table.
Unlike Task 1, employee records are not stored in a Python list.
Because the records are stored in MySQL, they remain available after restarting the FastAPI application.

Testing-
The APIs were tested using Swagger UI.
The following scenarios were tested:

Successful employee creation
Get all employees
Get employee by ID
Update employee
Duplicate email validation
Case-insensitive duplicate email validation
Blank/whitespace field validation
Get non-existing employee
Update non-existing employee
Delete employee
Get deleted employee
Database persistence after application restart

Screenshots of the API testing results are included in the screenshots folder.


Database Persistence-

An employee was created and stored in MySQL.
The FastAPI application was stopped and restarted.
After restarting the application, the same employee was successfully retrieved using the GET employee-by-ID API.
This confirms that employee data is stored persistently in the MySQL database.


What I Learned-
Through this task, I learned:

How to connect FastAPI with MySQL.
How SQLAlchemy is used to interact with a database.
How to create a database model using SQLAlchemy.
How to manage database sessions.
How to perform CRUD operations using a database.
How to use Pydantic for request and response validation.
How to handle database errors and rollback failed changes.
How to verify database persistence after restarting an application.
How to use Swagger UI for API testing.
How to maintain project changes using Git.


Difficulties Faced-
Initially, I had difficulty understanding SQLAlchemy, database sessions and connecting FastAPI with MySQL.
Understanding how the API communicates with the database was also difficult at first.
Testing the APIs through Swagger UI and checking the records in MySQL Workbench helped me understand the database flow better.

Assumptions-
Employee data used for testing is fictional.
MySQL is running locally on the development machine.
Database connection details are stored in the local .env file.
Authentication, frontend, Docker, relationships and database migrations are not implemented because they are not required for this task.