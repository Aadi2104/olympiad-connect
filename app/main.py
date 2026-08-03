from fastapi import FastAPI

from app.core.error_handlers import register_all_errors
from app.routers.analytics_routes import analytics_router
from app.routers.application_routes import application_router
from app.routers.olympiad_routes import olympiad_router
from app.routers.student_profile_routes import student_profile_router
from app.routers.user_routes import user_router

app= FastAPI(title="Olympiad Connect API",
    description="""
Olympiad Connect is a backend API for managing Olympiads, student profiles,
applications, authentication, and analytics.

Built using FastAPI, PostgreSQL, SQLAlchemy, and JWT Authentication.
""",
    version="1.0.0"
)

API_VERSION = "api/v1"

register_all_errors(app)

app.include_router(user_router,prefix=f"/{API_VERSION}/user",tags=["Users"])
app.include_router(olympiad_router,prefix=f"/{API_VERSION}/olympiad",tags=["Olympiads"])
app.include_router(application_router,prefix=f"/{API_VERSION}/application", tags=["Applications"])
app.include_router(student_profile_router, prefix=f"/{API_VERSION}/student_profile", tags=["Student Profiles"])
app.include_router(analytics_router,prefix=f"/{API_VERSION}/dashboard",tags=["Analytics"])

@app.get("/" , include_in_schema=False)
def get():
    return {
        "name": "Olympiad Connect API",
    "version": "1.0.0",
    "status": "running",
    "documentation": "/docs",
    "redoc": "/redoc",
    }
    
    