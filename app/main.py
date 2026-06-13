from fastapi import FastAPI
from .db.session import get_db
from .core.config import settings
from app.core.error_handlers import register_all_errors
from app.routers.user_routes import user_router
from app.routers.olympiad_routes import olympiad_router
from app.routers.application_routes import application_router
from app.routers.student_profile_routes import student_profile_router




app= FastAPI()

register_all_errors(app)

app.include_router(user_router,prefix="/user",tags=["Users"])
app.include_router(olympiad_router,prefix="/olympiad",tags=["Olympiads"])
app.include_router(application_router,prefix="/application", tags=["Applications"])
app.include_router(student_profile_router, prefix="/student_profile", tags=["StudentProfile"])

@app.get("/")
def get():
    return {
        "Mission":"For Miney"
    }
    