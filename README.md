# Employee Management API

# Project Overview

This project is a FastAPI backend application used to manage employee records.
It provides REST APIs to create, view, update and delete employee information.
Employee data is temporarily stored in a Python list. No database is used in this project.

# Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Swagger UI
- Git

# Features

- Create a new employee
- View all employees
- View an employee by ID
- Update employee details
- Delete an employee
- Check application health
- Validate employee input
- Validate email format
- Ensure email addresses are unique
- Restrict work mode to WFH or WFO
- Validate employee ID
- Return appropriate HTTP error responses

# Setup and Installation

1. Create a virtual environment
text:
py -3.12 -m venv venv
2. Activate the virtual environment
venv\Scripts\activate
3. Install the required packages
pip install -r requirements.txt
4. Run the FastAPI application
uvicorn main:app --reload
5. Open Swagger UI
http://127.0.0.1:8000/docs


API Endpoints----

Method  /Endpoint       /Description

GET	    /health         /Check application health
POST    /employees	    /Create a new employee
GET     /employees	    /Get all employees
GET	    /employees/{id}	/Get an employee by ID
PUT	    /employees/{id}	/Update employee details
DELETE	/employees/{id}	/Delete an employee

Validation Rules--

Employee name is required.
Email must be in a valid email format.
Email addresses must be unique.
Department is required.
Primary skill is required.
Location is required.
Work mode must be either WFH or WFO.
Employee ID must be greater than 0.
A 404 Not Found response is returned when an employee does not exist.
A 400 Bad Request response is returned when a duplicate email is used.


Data Storage--

Employee records are stored temporarily in a Python list in memory.
No database is used in this project.
Because the data is stored in memory, employee records added through the API are lost when the application is restarted.
Five sample employee records are hardcoded in the application for testing.

What I Learned--

Through this project, I learned:

How to create REST APIs using FastAPI.
How to define and validate request data using Pydantic.
How to use HTTP methods such as GET, POST, PUT and DELETE.
How CRUD operations work in a backend application.
How to use Swagger UI to test APIs.
How to handle validation and HTTP errors.
How to use Git and maintain a project repository.


Difficulties Faced--

Understanding API concepts, request validation and error handling was difficult at first.
Testing each API using Swagger UI helped me understand how the backend works and how different requests and responses are handled.

Assumptions--

No database is used in this project.
Employee data is stored temporarily in a Python list.
Five sample employee records are hardcoded for testing.
Data stored in memory will be lost when the application is restarted.
Email addresses must be unique.
Work mode can only be WFH or WFO