from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.core.errors import (
    UserAlreadyExists,
    UserNotExist,
    InvalidCredentials,
    InvalidToken,
    TokenNotFound,
    NotAuthorized,
    InvalidDateConfiguration,
    OlympiadNotExists,
    OlympiadAlreadyInactive,
    ApplicationAlreadyExists,
    OlympiadInactive,
    RegistrationClosed,
    RegistrationNotStarted,
    ApplicationNotExists,
    ProfileNotCompleted,
    ProfileAlreadyExists,
    ProfileDataAlreadyExists,
    ProfileNotExists,
    ApplicationAlreadyReviewed,
    OlympiadAlreadyActive,
    TokenExpired,
    InvalidOTP,
    OTPRequired,
    InvalidPassword,
    UserAlreadyHasRole,
    SuperAdminModificationNotAllowed,
    UserStatusConflict
)




def user_already_exists_handler(request: Request, exc: UserAlreadyExists):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT, content={"detail": "User already exists"}
    )


def user_not_exist_handler(request: Request, exc: UserNotExist):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
    )


def invalid_credentials_handler(request: Request, exc: InvalidCredentials):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid credentials"}
    )


def token_not_found_handler(request: Request, exc: TokenNotFound):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Access token is required"}
    )


def invalid_token_handler(request: Request, exc: InvalidToken):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)}
    )
    
def not_authorized_handler(request:Request, exc:NotAuthorized):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "You are not authorized to perform this action"}
    )
    
def invalid_date_configuration_handler(request:Request, exc:InvalidDateConfiguration):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail":str(exc)
        }
    )
    
def olympiad_not_exists_handler(request:Request, exc:OlympiadNotExists):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Olympiad not found"}
        
    )

def olympiad_already_inactive_handler(request:Request,exc:OlympiadAlreadyInactive):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail":"Olympiad is already inactive"
        }
    )
    
def application_already_exists_handler(request:Request,exc:ApplicationAlreadyExists):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail":"Application already exists"}
    )

def olympiad_inactive_handler(request:Request,exc:OlympiadInactive):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Olympiad is currently inactive"}
    )

def registration_not_started_handler(request:Request,exc:RegistrationNotStarted):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Registration has not started yet"}
    )

def registration_closed_handler(request:Request,exc:RegistrationClosed):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Registration has ended"}
    )

def application_not_exists_handler(request:Request,exc:ApplicationNotExists):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Application not found"}
    )
    
def profile_not_completed_handler(request:Request, exc:ProfileNotCompleted):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "Student profile is incomplete"}
    )

def profile_already_exists_handler(request : Request , exc:ProfileAlreadyExists):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Profile already exists"}
    )
    
def profile_data_already_exists_handler(request:Request,exc:ProfileDataAlreadyExists):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "A profile with the provided details already exists"}
    )

def profile_not_exists_handler(request:Request , exc:ProfileNotExists):
    return JSONResponse(
        status_code= status.HTTP_404_NOT_FOUND,
        content={"detail": "Profile not found"}
    )

def application_already_reviewed_handler(request:Request, exc:ApplicationAlreadyReviewed):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail":"Application has already been reviewed"
        }
    )

def olympiad_already_active_handler(request:Request, exc:OlympiadAlreadyActive):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail":"Olympiad already active"
        }
    )
    
def token_expired_handler(request:Request, exc:TokenExpired):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail":str(exc)}
    )
    
def invalid_otp_handler(request:Request, exc:InvalidOTP):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail":"Enter correct otp"}
    )

def otp_required_handler(request:Request, exc:OTPRequired):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail":"Otp is required"}
    )
def invalid_password_handler(request:Request, exc:InvalidPassword):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"details":"Password does not match"}
    )

def user_already_has_role_handler(request:Request, exc:UserAlreadyHasRole):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail":str(exc)}
    )

def super_admin_modification_not_allowed_handler(request:Request, exc:SuperAdminModificationNotAllowed):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail":"Super admin accounts cannot be modified"
        }
    )
def user_status_conflict_handler(request:Request, exc:UserStatusConflict):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "detail":str(exc)
        }
    )

def register_all_errors(app: FastAPI):
    app.add_exception_handler(UserAlreadyExists, user_already_exists_handler)
    
    app.add_exception_handler(UserNotExist, user_not_exist_handler)

    app.add_exception_handler(InvalidCredentials, invalid_credentials_handler)

    app.add_exception_handler(TokenNotFound, token_not_found_handler)

    app.add_exception_handler(InvalidToken, invalid_token_handler)
    
    app.add_exception_handler(NotAuthorized,not_authorized_handler)
    
    app.add_exception_handler(InvalidDateConfiguration,invalid_date_configuration_handler)
    
    app.add_exception_handler(OlympiadNotExists,olympiad_not_exists_handler)
    
    app.add_exception_handler(OlympiadAlreadyInactive,olympiad_already_inactive_handler)
    
    app.add_exception_handler(ApplicationAlreadyExists,application_already_exists_handler)
    
    app.add_exception_handler(OlympiadInactive,olympiad_inactive_handler)
    
    app.add_exception_handler(RegistrationNotStarted,registration_not_started_handler)
    
    app.add_exception_handler(RegistrationClosed,registration_closed_handler)
    
    app.add_exception_handler(ApplicationNotExists,application_not_exists_handler)
    
    app.add_exception_handler(ProfileNotCompleted,profile_not_completed_handler)
    
    app.add_exception_handler(ProfileAlreadyExists,profile_already_exists_handler)
    
    app.add_exception_handler(ProfileDataAlreadyExists,profile_data_already_exists_handler)
    
    app.add_exception_handler(ProfileNotExists,profile_not_exists_handler)
    
    app.add_exception_handler(ApplicationAlreadyReviewed,application_already_reviewed_handler)
    
    app.add_exception_handler(OlympiadAlreadyActive,olympiad_already_active_handler)
    
    
    app.add_exception_handler(TokenExpired,token_expired_handler)
    
    app.add_exception_handler(InvalidOTP,invalid_otp_handler)
    
    app.add_exception_handler(OTPRequired,otp_required_handler)
    
    app.add_exception_handler(InvalidPassword,invalid_password_handler)
    
    app.add_exception_handler(UserAlreadyHasRole,user_already_has_role_handler)
    
    app.add_exception_handler(SuperAdminModificationNotAllowed,super_admin_modification_not_allowed_handler)
    
    app.add_exception_handler(UserStatusConflict,user_status_conflict_handler)
    
    