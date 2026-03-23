from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="SDR") # Admin, SDR, Manager

    leads = relationship("Lead", back_populates="assigned_sdr")
    deals = relationship("Deal", back_populates="assigned_sdr")

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True, nullable=True)
    company = Column(String, index=True, nullable=True)
    lead_source = Column(String, default="Manual")
    
    # AI specific fields
    ai_priority = Column(String, nullable=True) # High, Medium, Low
    ai_score = Column(Integer, nullable=True)
    ai_next_action = Column(String, nullable=True)
    
    status = Column(String, default="new") # new, scored, contacted, closed
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assigned_sdr_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    assigned_sdr = relationship("User", back_populates="leads")
    tasks = relationship("Task", back_populates="lead")
    deals = relationship("Deal", back_populates="lead")
    action_logs = relationship("ActionLog", back_populates="lead")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    due_time = Column(DateTime, nullable=True)
    assigned_sdr_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="open") # open, completed
    created_at = Column(DateTime, default=datetime.utcnow)

    lead = relationship("Lead", back_populates="tasks")
    assigned_sdr = relationship("User")

class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    value = Column(Float, default=0.0)
    stage = Column(String, index=True, default="Lead") # Lead, In Progress, Negotiation, Closed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    assigned_sdr_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    lead = relationship("Lead", back_populates="deals")
    assigned_sdr = relationship("User", back_populates="deals")

class ActionLog(Base):
    __tablename__ = "action_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    action_type = Column(String) # Escalation, Notification, Follow-up
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    lead = relationship("Lead", back_populates="action_logs")
