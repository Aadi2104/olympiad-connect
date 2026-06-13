from pydantic import BaseModel, field_validator, model_validator,ConfigDict
from datetime import datetime
from typing import Optional

class OlympiadCreateModel(BaseModel):
    title: str
    description: str
    registration_start: datetime
    registration_end: datetime
    exam_date: datetime

    @field_validator(
        "registration_start", "registration_end", "exam_date", mode="before"
    )
    @classmethod
    def convert(cls, value: str | datetime):
        if isinstance(value, str):
            return datetime.strptime(value, "%d-%m-%Y %H:%M")
        return value

    @model_validator(mode="after")
    def check_dates(self):
        if self.registration_end <= self.registration_start:
            raise ValueError(
                "Registration end date cannot be before registration start date"
            )
        if self.registration_end >= self.exam_date:
            raise ValueError("Exam date must be after registration end date")

        return self


class OlympiadResponseModel(BaseModel):
    id: int
    title: str
    description: str
    registration_start: datetime
    registration_end: datetime
    exam_date: datetime
    created_by_id : int | None
    
    model_config = ConfigDict(from_attributes=True)
    
    
class OlympiadUpdateModel(BaseModel):
    title:Optional[str] = None
    description: Optional[str] = None
    registration_start:Optional[datetime] = None
    registration_end:Optional[datetime] = None
    exam_date:Optional[datetime] = None

    @field_validator(
        "registration_start", "registration_end", "exam_date", mode="before"
    )
    @classmethod
    def convert(cls, value: str | datetime):
        if isinstance(value, str):
            return datetime.strptime(value, "%d-%m-%Y %H:%M")
        return value


class OlympiadDeleteResponseModel(BaseModel):
    id: int
    title: str
    description: str
    is_active : bool
    registration_start: datetime
    registration_end: datetime
    exam_date: datetime
    created_by_id : int | None
    
    model_config = ConfigDict(from_attributes=True)