#Employee Management API

#About This Project-

I am a beginner in FastAPI, and I created this project to learn how a simple backend API works.
This project is used to create, view, update and delete employee details.
The employee data is stored temporarily in a Python list. No database is used.

#For Beginners-

This README is written in simple English so that new learners can understand and run the project easily.

#Technologies Used-

- Python
- FastAPI
- Pydantic
- Uvicorn
- Swagger UI

#Features-

- Create employee
- Get all employees
- Get employee by ID
- Update employee
- Delete employee
- Health check
- Email validation
- Duplicate email check
- Employee ID validation
- 404 error handling

#API Endpoints-

| Method | Endpoint | Use |

| GET | /health | Check application |
| POST | /employees | Create employee |
| GET | /employees | Get all employees |
| GET | /employees/{id} | Get one employee |
| PUT | /employees/{id} | Update employee |
| DELETE | /employees/{id} | Delete employee |

##How to Run-

Create virtual environment:
--text
py -3.12 -m venv venv

Activate venv:

venv\Scripts\activate

Install packages:

pip install -r requirements.txt

Start the server:

uvicorn main:app --reload

Open Swagger:

http://127.0.0.1:8000/docs

Sample Data-

Five sample employees are added directly in the code for testing.

Tulasi
Veera
Pramodh
Pranay
Hemanth

What I Learned-

As a beginner, I learned how FastAPI, APIs, CRUD operations, Pydantic validation and Swagger UI work.
I also learned how to handle errors and store data temporarily using a Python list.

Difficulties Faced-

Understanding APIs, validation and error handling was difficult at first.
Testing each API using Swagger helped me understand them better.

Assumptions-
No database is used.
Employee data is stored in a Python list.
Five sample records are hardcoded for testing.
Data will be lost when the application is restarted.
Email must be unique.
Work mode can only be WFH or WFO.


