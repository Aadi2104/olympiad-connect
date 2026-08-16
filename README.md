# 🏆 Olympiad Connect

<div align="center">

### A production-oriented FastAPI backend for managing Olympiads, built while exploring real-world backend engineering concepts.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-orange)
![JWT](https://img.shields.io/badge/JWT-Authentication-success)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-blueviolet)

🚀 **30+ REST APIs • JWT • Refresh Tokens • HTTPBearer • RBAC • PostgreSQL • SQLAlchemy • Alembic**

</div>

---

# 🚀 Overview

Olympiad Connect is a **FastAPI-powered backend application** designed to simplify Olympiad management for students and administrators.

Rather than being a simple CRUD application, this project focuses on applying **real-world backend engineering concepts** while learning and improving with FastAPI. It demonstrates authentication, authorization, refresh-token lifecycle management, modular architecture, database design, email workflows, analytics, API documentation, and production-oriented backend practices.

The project continuously evolves as new backend concepts are explored, implemented, debugged, and refined.

---

# 📌 Project Snapshot

| Item | Details |
|------|---------|
| 🚧 Status | Actively Developed |
| 🚀 REST APIs | 30+ |
| 👥 User Roles | Student · Admin · Super Admin |
| 🏗️ Architecture | Layered & Service-Based |
| 🔐 Authentication | JWT + Refresh Tokens + HTTPBearer |
| 🗄️ Database | PostgreSQL |
| 📦 ORM | SQLAlchemy |
| 📧 Email | FastAPI-Mail |
| ⚙️ Background Processing | FastAPI BackgroundTasks |
| 📖 Documentation | Swagger UI & ReDoc |

---

# 🎯 Why Olympiad Connect?

While learning FastAPI, I wanted to build something beyond tutorial-based CRUD applications.

Olympiad Connect was created to explore how production-style backend systems are designed by implementing concepts such as:

- Secure Authentication
- Refresh Token Lifecycle Management
- Role-Based Authorization
- Modular Architecture
- Database Migrations
- Email Verification Workflows
- Background Tasks
- Analytics
- Service Layer Design
- Clean API Architecture

The goal is not only to build a functional application but also to continuously improve it by adopting backend engineering best practices.

---

# 🎯 Design Goals

The primary objectives of this project are:

- Build maintainable and scalable REST APIs.
- Design a modular backend architecture.
- Apply secure authentication and authorization.
- Implement a complete refresh-token lifecycle.
- Gain practical experience with SQLAlchemy ORM.
- Explore PostgreSQL database design.
- Learn database versioning using Alembic.
- Apply asynchronous/background processing where appropriate.
- Follow clean coding and separation-of-concerns practices.
- Build a backend that can continue evolving with additional features.

---

# 🏗️ System Architecture

```text
                    Client
                       │
                       ▼
                 FastAPI Routers
                       │
          Authentication / Authorization
                       │
                Dependency Injection
                       │
                  Service Layer
                       │
          SQLAlchemy ORM & Models
                       │
                   PostgreSQL
                       ▲
                    Alembic
```

### Architecture Overview

The application follows a **layered architecture** where responsibilities are separated across routers, services, schemas, models, and the database layer.

This structure keeps the codebase modular, maintainable, and easier to extend as the project grows.

---

# 📂 Project Structure

```text
olympiad-connect/
│
├── app/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── alembic/
├── assets/
├── requirements.txt
├── README.md
├── .env.example
└── alembic.ini
```

### Folder Responsibilities

| Folder | Responsibility |
|---------|----------------|
| `core` | Configuration, security, authentication, shared utilities |
| `db` | Database connection and session management |
| `models` | SQLAlchemy ORM models |
| `routers` | API endpoints |
| `schemas` | Pydantic request and response models |
| `services` | Business logic and application workflows |
| `utils` | Helper utilities |

---

# ✨ Features

Olympiad Connect is built around multiple backend modules, each responsible for a specific part of the system.

## 🔐 Authentication & Authorization

- JWT Authentication
- HTTPBearer Protected Routes
- Access Token Generation
- Refresh Token Generation
- JTI-Based Refresh Session Identification
- Hashed Refresh Token Storage
- Refresh Token Validation
- Refresh Token Rotation
- Server-Side Token Revocation
- Secure Logout
- Role-Based Access Control (RBAC)
- Email Verification
- Password Reset Workflow
- Protected Administrative Endpoints

### Refresh Token Lifecycle

The refresh-token implementation uses PostgreSQL-backed server-side sessions.

```text
Login
  │
  ├── Access Token
  │
  └── Refresh Token + JTI
            │
            ▼
      Hash & Store in DB
            │
            ▼
       Refresh Request
            │
            ▼
      Decode Refresh Token
            │
            ▼
        Extract JTI
            │
            ▼
      Find DB Session
            │
            ▼
   Validate Expiry / Revocation
            │
            ▼
       Verify Token Hash
            │
            ▼
        Check User
            │
            ▼
      Revoke Old Token
            │
            ▼
    Generate New Tokens
            │
            ▼
     Store New Session
            │
            ▼
          Commit
```

### Refresh Token Security

- Raw refresh tokens are not stored in PostgreSQL.
- Refresh tokens are stored as hashes.
- JTI uniquely identifies the corresponding refresh session.
- Revoked refresh tokens cannot be reused.
- Successful refresh requests rotate the refresh token.
- Old-token revocation and new-token creation are committed transactionally.
- UTC-aware timestamps are used for refresh-session expiry handling.

---

## 👥 User Management

- User Registration
- User Login
- User Profile Management
- Activate / Deactivate Users
- Promote / Demote Administrators
- Super Admin Privileges

---

## 🎓 Student Profile Management

- Create Student Profiles
- View Student Profiles
- Update Student Information
- Profile Completion Tracking
- Admin Access to Student Profiles

---

## 🏆 Olympiad Management

- Create Olympiads
- Update Olympiad Details
- Activate / Deactivate Olympiads
- View Available Olympiads

---

## 📝 Application Management

- Submit Olympiad Applications
- View Submitted Applications
- View Individual Applications
- Review Applications
- Approve / Reject Applications
- Track Application Status
- Filter Applications by Olympiad
- View Pending Applications

---

## 📊 Analytics Dashboard

- User Statistics
- Student Statistics
- Olympiad Statistics
- Application Statistics
- Pending Applications
- Approved Applications
- Rejected Applications
- Dashboard Metrics
- Approval Rate

---

## 📧 Email & Background Processing

- Email Verification
- Password Reset Email Workflow
- FastAPI-Mail Integration
- SMTP-based Email Delivery
- Background Tasks for appropriate non-blocking operations

---

# 🛠️ Tech Stack

| Category | Technologies |
|-----------|--------------|
| **Language** | Python |
| **Framework** | FastAPI |
| **Validation** | Pydantic |
| **Authentication** | JWT, HTTPBearer |
| **Refresh Tokens** | JTI, Hashed Token Storage, Rotation, Revocation |
| **Password Security** | Passlib |
| **Token Management** | itsdangerous |
| **Email Services** | FastAPI-Mail, aiosmtplib |
| **Background Processing** | FastAPI BackgroundTasks |
| **ORM** | SQLAlchemy |
| **Database** | PostgreSQL |
| **Migrations** | Alembic |
| **Configuration** | Pydantic Settings, Python Dotenv |
| **API Documentation** | Swagger UI, ReDoc |
| **ASGI Server** | Uvicorn |
| **Version Control** | Git & GitHub |

---

# 🧠 Backend Concepts Implemented

This project explores backend engineering concepts beyond basic CRUD operations.

### 🏗️ Architecture

- Layered Architecture
- Modular Project Structure
- Service Layer Pattern
- Separation of Concerns
- Dependency Injection

### 🌐 API Design

- RESTful API Development
- Request Validation
- Response Validation
- Standardized API Responses
- Interactive API Documentation

### 🔐 Security

- JWT Authentication
- HTTPBearer Authentication
- Access & Refresh Token Lifecycle
- JTI-Based Session Identification
- Hashed Refresh Token Storage
- Refresh Token Rotation
- Server-Side Revocation
- Role-Based Access Control (RBAC)
- Password Hashing
- Email Verification
- Password Reset Tokens

### 🗄️ Database

- SQLAlchemy ORM
- PostgreSQL
- Database Relationships
- Server-Side Refresh Sessions
- Alembic Database Migrations
- Transaction-Safe Token Rotation

### ⚙️ Backend Practices

- Dependency Injection
- Environment-Based Configuration
- Background Tasks
- Modular Code Organization
- Configuration Management
- Custom Exception Handling
- Reusable Request / Response Models

---

# 🔒 Security Features

Security is one of the primary focuses of Olympiad Connect.

### Authentication

- JWT-based Authentication
- HTTPBearer Protected Endpoints
- Access Token Generation
- Refresh Token Rotation
- Refresh Token Validation
- Server-Side Refresh Sessions
- Token Revocation

### Authorization

- Role-Based Access Control
- Student Access
- Admin Access
- Super Admin Access

### Password Security

- Password Hashing using Passlib
- Secure Password Verification

### Account Protection

- Email Verification
- Password Reset Workflow
- User Activation / Deactivation
- Protected Administrative APIs

---

# 📈 Project Highlights

- 🚀 30+ REST APIs
- 👥 3 User Roles
- 📂 6 Backend Modules
- 🔐 JWT + HTTPBearer Authentication
- 🔄 Refresh Token Rotation
- 🆔 JTI-Based Refresh Sessions
- 🔒 Hashed Refresh Token Storage
- 🚫 Server-Side Token Revocation
- 🛡️ RBAC Implementation
- 📧 Email Verification
- ⚙️ Background Tasks
- 🔄 Password Reset Workflow
- 📊 Analytics Dashboard
- 🗄️ PostgreSQL Database
- ⚡ SQLAlchemy ORM
- 🔄 Alembic Database Migrations
- 📖 Swagger UI & ReDoc Documentation

---

# 📚 Backend Modules

Olympiad Connect is organized into independent backend modules, each responsible for a specific part of the application.

| Module | Description |
|---------|-------------|
| 🔐 Authentication | Registration, login, JWT authentication, refresh tokens, token validation, logout, email verification, and password reset workflows. |
| 👥 Users | User management, role management, account activation, and administrative operations. |
| 🎓 Student Profiles | Create, update, retrieve, and manage student profile information. |
| 🏆 Olympiads | Create, update, activate, deactivate, and manage Olympiad details. |
| 📝 Applications | Submit applications, review submissions, approve/reject requests, and track application status. |
| 📊 Analytics | Dashboard metrics, user statistics, Olympiad statistics, application statistics, and approval rate analytics. |

> 📖 Every module follows the same layered architecture using **Routers → Services → Models → Database**, making the project modular, maintainable, and scalable.

---

# 🔄 Request Lifecycle

Every API request follows a structured flow before a response is returned.

```text
                HTTP Request
                      │
                      ▼
              FastAPI Router
                      │
                      ▼
        Dependency Injection Layer
(Authentication • Authorization • Validation)
                      │
                      ▼
              Service Layer
(Business Logic & Application Rules)
                      │
                      ▼
            SQLAlchemy ORM
                      │
                      ▼
               PostgreSQL
                      │
                      ▼
        Pydantic Response Model
                      │
                      ▼
               HTTP Response
```

### Request Flow

1. The client sends an HTTP request.
2. FastAPI routes the request to the appropriate endpoint.
3. Dependencies validate authentication, authorization, and request data.
4. Business logic is executed inside the service layer.
5. SQLAlchemy communicates with PostgreSQL.
6. Data is validated using Pydantic response models.
7. A structured HTTP response is returned to the client.

---

# 🗄️ Database Design

The application uses PostgreSQL with SQLAlchemy ORM to model relationships between users, student profiles, Olympiads, applications, and refresh-token sessions.

```text
                    Users
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
 Student Profiles  Applications  Refresh Sessions
                        │
                        ▼
                    Olympiads
```

### Relationship Overview

- One User can own one Student Profile.
- One Student can submit multiple Applications.
- One Olympiad can receive multiple Applications.
- One User can have multiple refresh-token sessions.
- Refresh-token sessions store JTI, token hash, expiry, and revocation state.
- Admins manage Olympiads and Applications.
- Super Admins manage administrative users and system-level operations.

---

# ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Aadi2104/olympiad-connect.git
cd olympiad-connect
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv .venv
```

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file using the provided `.env.example`.

### 5️⃣ Apply Database Migrations

```bash
alembic upgrade head
```

### 6️⃣ Run the Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- Swagger UI → `http://localhost:8000/docs`
- ReDoc → `http://localhost:8000/redoc`

---

# 🔑 Environment Variables

Create a `.env` file inside the project root.

```env
# Database
DATABASE_URL=

# Authentication
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRY_MINUTES=

# Email Verification
SIGNUP_TOKEN_EXPIRY_MINUTES=
RESET_PASSWORD_TOKEN_EXPIRY_MINUTES=

# Mail Configuration
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_FROM_NAME=
MAIL_SERVER=
MAIL_PORT=
MAIL_STARTTLS=
MAIL_SSL_TLS=
```

> ⚠️ Never commit your `.env` file. Keep sensitive credentials private and use `.env.example` as the template.

---

# 📸 Project Preview

The following screenshots provide a quick overview of the project's structure and API documentation.

## 🏠 Project Structure

> Modular folder structure following a layered architecture.

![Project Structure](assets/screenshots/project-structure.png)

---

## 📖 Swagger UI

> Interactive API documentation for testing and exploring endpoints.

![Swagger UI](assets/screenshots/swagger-overview.png)

---

## 📚 ReDoc Documentation

> Clean and detailed API reference generated automatically by FastAPI.

![ReDoc](assets/screenshots/redoc-overview.png)

---

## 📊 Analytics Dashboard API

> Example analytics response showcasing dashboard metrics.

![Analytics](assets/screenshots/analytics-dashboard.png)

---

# 📈 Project Statistics

| Metric | Value |
|---------|------:|
| 🚀 REST APIs | 30+ |
| 📂 Backend Modules | 6 |
| 👥 User Roles | 3 |
| 🛡️ Authentication | JWT + Refresh Tokens + HTTPBearer |
| 🗄️ Database | PostgreSQL |
| ⚡ ORM | SQLAlchemy |
| 🔄 Database Migrations | Alembic |
| 📧 Email | FastAPI-Mail |
| ⚙️ Background Processing | FastAPI BackgroundTasks |
| 📖 API Documentation | Swagger UI & ReDoc |

---

# 🛣️ Roadmap

## ✅ Completed

- JWT Authentication
- HTTPBearer Authentication
- Access Token Generation
- Refresh Token Authentication
- JTI-Based Refresh Sessions
- Hashed Refresh Token Storage
- Refresh Token Rotation
- Server-Side Token Revocation
- Secure Logout
- Role-Based Access Control (RBAC)
- Email Verification
- Password Reset Workflow
- Background Tasks
- User Management
- Student Profile Module
- Olympiad Management
- Application Management
- Analytics Dashboard
- PostgreSQL Integration
- SQLAlchemy ORM
- Alembic Database Migrations
- Swagger UI & ReDoc Documentation

---

## 🚧 Currently Working On

- API Response Improvements
- Expanding Automated Testing Coverage

---

## 📅 Planned

- API Testing with Pytest
- Docker Support
- CI/CD Pipeline
- Cloud Deployment
- AI-Powered Features
- Performance Optimizations
- Advanced Session Management
- Refresh-Token Reuse Detection

---

# 💡 Learning Outcomes

Building Olympiad Connect has helped me gain practical experience with:

- FastAPI Backend Development
- RESTful API Design
- Layered and Service-Based Architecture
- JWT Authentication
- Refresh Token Lifecycle Management
- JTI-Based Server-Side Sessions
- Token Hashing and Revocation
- Role-Based Access Control
- SQLAlchemy ORM
- PostgreSQL Database Design
- Alembic Database Migrations
- Email Verification and Password Reset Workflows
- Background Tasks
- Custom Exception Handling
- API Documentation with Swagger UI and ReDoc
- Backend Security and Transaction Safety

---

# 🚀 Future Vision

Olympiad Connect is an evolving backend project.

The goal is to continue improving it by implementing production-oriented backend features such as automated testing, Docker, CI/CD, cloud deployment, advanced session management, performance optimizations, and AI-powered capabilities while continuously exploring modern backend engineering practices.

---

# 🌟 About This Project

This project was not built after mastering FastAPI.

It was built **while learning FastAPI**, with every feature representing a new concept explored, implemented, debugged, and refined.

Instead of following isolated tutorials, the focus has always been on applying backend engineering concepts to a real-world application. As new technologies and best practices are learned, they are integrated into the project, making Olympiad Connect a continuously evolving backend system.

---

# 🤝 Contributing

Contributions, ideas, suggestions, and feedback are always welcome.

If you'd like to improve Olympiad Connect:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

<div align="center">

### ⭐ If you found this project interesting, consider giving it a star!

**Thank you for visiting Olympiad Connect! 🚀**

</div>
