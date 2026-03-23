from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "SDR"

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True

class ActionLogBase(BaseModel):
    action_type: str
    description: str

class ActionLogCreate(ActionLogBase):
    pass

class ActionLog(ActionLogBase):
    id: int
    lead_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_time: Optional[datetime] = None
    assigned_sdr_id: Optional[int] = None
    status: str = "open"

class TaskCreate(TaskBase):
    lead_id: int

class Task(TaskBase):
    id: int
    lead_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

class DealBase(BaseModel):
    title: str
    value: float = 0.0
    stage: str = "Lead"
    assigned_sdr_id: Optional[int] = None

class DealCreate(DealBase):
    pass

class Deal(DealBase):
    id: int
    created_at: datetime
    lead_id: Optional[int] = None

    class Config:
        from_attributes = True
        orm_mode = True

class LeadBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    
    lead_source: str = "Manual"
    ai_priority: Optional[str] = None
    ai_score: Optional[int] = None
    ai_next_action: Optional[str] = None
    status: str = "new"
    assigned_sdr_id: Optional[int] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    ai_priority: Optional[str] = None
    ai_score: Optional[int] = None
    ai_next_action: Optional[str] = None
    status: Optional[str] = None

class Lead(LeadBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tasks: List[Task] = []
    deals: List[Deal] = []
    action_logs: List[ActionLog] = []

    class Config:
        from_attributes = True
        orm_mode = True
