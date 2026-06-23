from fastapi import FastAPI
from .db.session import get_db
from .core.config import settings
from app.core.error_handlers import register_all_errors
from app.routers.user_routes import user_router
from app.routers.olympiad_routes import olympiad_router
from app.routers.application_routes import application_router
from app.routers.student_profile_routes import student_profile_router
from app.routers.analytics_routes import analytics_router



app= FastAPI()

API_VERSION = "api/v1"

register_all_errors(app)

app.include_router(user_router,prefix=f"/{API_VERSION}/user",tags=["Users"])
app.include_router(olympiad_router,prefix=f"/{API_VERSION}/olympiad",tags=["Olympiads"])
app.include_router(application_router,prefix=f"/{API_VERSION}/application", tags=["Applications"])
app.include_router(student_profile_router, prefix=f"/{API_VERSION}/student_profile", tags=["StudentProfile"])
app.include_router(analytics_router,prefix=f"/{API_VERSION}/dashboard",tags=["Analytics"])

@app.get("/")
def get():
    return {
        "name": "Olympiad Connect",
        "version": "v1",
        "status": "running",
        "description": "Backend API for managing Olympiads, student profiles, and applications."
    }
    
    