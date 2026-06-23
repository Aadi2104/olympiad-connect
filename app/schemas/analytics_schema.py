from pydantic import BaseModel, ConfigDict


class DashboardAnalyticsResponseModel(BaseModel):
    total_users: int
    total_students: int
    total_admins: int
    active_users: int

    total_olympiads: int
    active_olympiads: int
    
    total_applications: int
    pending_applications: int
    approved_applications: int
    rejected_applications: int
    
    approval_rate: float
    
    completed_profiles: int
    
    model_config = ConfigDict(from_attributes=True)
