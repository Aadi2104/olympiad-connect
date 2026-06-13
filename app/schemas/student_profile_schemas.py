from pydantic import BaseModel, field_validator , ConfigDict
from app.models.student_profile_model import StudentGender
from datetime import date , datetime


class StudentProfileCreateModel(BaseModel):
    first_name: str
    last_name: str
    gender: StudentGender
    date_of_birth: date
    college_name: str
    semester: int
    enrollment_number: str
    branch: str
    phone_number: str


    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, value:str):
        value = value.strip()
        if len(value) < 3:
            raise ValueError("First name is too short")
        return value
        
    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value:str):
        value = value.strip()
        if len(value) < 3:
            raise ValueError("Last name is too short")
        return value
    
    @field_validator("semester")
    @classmethod
    def validate_semester(cls, value: int):
        if value < 1 or value > 8:
            raise ValueError("Semester should be between 1 and 8")

        return value
    
    @field_validator("enrollment_number")
    @classmethod
    def validate_enrollment(cls, value:str):
        value = value.strip()
        value= value.upper()
        if len(value) < 3:
            raise ValueError("Enter a valid enrollment number")
        return value
   
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls,value:str):
        value=value.strip()
        if not value.isdigit():
            raise ValueError("Phone number only consist of numbers")
        if len(value) != 10:
            raise ValueError("Phone number consist of 10 digits")
        
        return value
    
    
    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls,value:date):
        if value > date.today():
            raise ValueError("Enter correct Date of birth")
        
        return value
    

class StudentProfileResponseModel(BaseModel):
    id:int
    first_name: str
    last_name: str
    gender: StudentGender
    date_of_birth: date
    college_name: str
    semester: int
    enrollment_number: str
    branch: str
    phone_number: str
    
    model_config= ConfigDict(from_attributes=True)
    
class StudentProfilePhoneNumberUpdateModel(BaseModel):
    phone_number: str
    
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls,value:str):
        value=value.strip()
        if not value.isdigit():
            raise ValueError("Phone number only consist of numbers")
        if len(value) != 10:
            raise ValueError("Phone number consist of 10 digits")
        
        return value
    
    

class AdminStudentProfileResponseModel(BaseModel):
    
    id:int
    user_id : int
    first_name: str
    last_name: str
    gender: StudentGender
    date_of_birth: date
    college_name: str
    semester: int
    enrollment_number: str
    branch: str
    phone_number: str
    updated_at : datetime
   
    
    model_config= ConfigDict(from_attributes=True)