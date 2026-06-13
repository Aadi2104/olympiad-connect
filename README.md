Olympiad Connect

Olympiad Connect is a FastAPI-based backend application designed to manage Olympiad registrations, student profiles, and application review workflows. The system provides secure authentication, role-based access control, email verification, and administrative management capabilities.

Features

Authentication & Authorization

* User Registration with Email OTP Verification
* JWT-Based Authentication
* Forgot Password & Reset Password Functionality
* Secure Password Hashing
* Role-Based Access Control (RBAC)

User Roles

* Student
* Admin
* Super Admin

Student Profile Management

* Create Student Profile
* View Personal Profile
* Update Phone Number
* Admin Access to Student Profiles

Olympiad Management

* Create Olympiads
* Update Olympiad Details
* Deactivate Olympiads
* Reactivate Olympiads
* View Active Olympiads

Application Management

* Apply for Olympiads
* View Submitted Applications
* View Individual Application
* Approve Applications
* Reject Applications
* View Pending Applications
* Filter Applications by Olympiad

User Administration

* Activate User Accounts
* Deactivate User Accounts
* Promote Student to Admin
* Demote Admin to Student
* View All Users
* View All Admins

Additional Features

* Pagination Support
* Custom Exception Handling
* Alembic Database Migrations
* Layered Architecture (Routers, Services, Schemas, Models)

Tech Stack

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic
* JWT Authentication
* SMTP Email Service

Project Structure

app/
├── core/
├── db/
├── models/
├── routers/
├── schemas/
├── services/
└── main.py
alembic/
requirements.txt

Installation

Clone Repository

git clone https://github.com/Aadi2104/olympiad-connect.git
cd olympiad-connect

Create Virtual Environment

python -m venv venv
source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

Environment Variables

Create a .env file and configure the following variables:

DATABASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_SERVER=
MAIL_PORT=

Database Migration

alembic upgrade head

Run Application

fastapi dev app/main.py

or

uvicorn app.main:app --reload

API Documentation

Swagger UI:

http://localhost:8000/docs

ReDoc:

http://localhost:8000/redoc

User Roles & Permissions

Student

* Create and manage profile
* Apply for Olympiads
* View submitted applications

Admin

* Manage Olympiads
* Review applications
* Access student profiles

Super Admin

* Promote/Demote Admins
* Activate/Deactivate Users
* Manage platform users

Future Enhancements

* Refresh Token Authentication
* Docker Support
* Automated Testing with Pytest
* CI/CD Pipeline
* Rate Limiting
* Audit Logging
* Cloud Deployment

Learning Outcomes

This project helped in understanding:

* FastAPI Backend Development
* REST API Design
* JWT Authentication
* Role-Based Access Control
* SQLAlchemy ORM
* Alembic Migrations
* Email Verification Workflows
* Backend Project Architecture
* API Security Best Practices

Author

Aaditya