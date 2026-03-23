from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)

@router.get("/dashboard")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    today = date.today()
    
    # Total Leads Today
    total_leads_today = db.query(models.Contact).filter(
        func.date(models.Contact.created_at) == today
    ).count()
    
    # High Priority Leads
    high_priority_leads = db.query(models.Contact).filter(
        models.Contact.priority == "High",
        models.Contact.status != "Closed"
    ).count()
    
    # Average Response Time (in minutes) for contacted leads
    contacted_leads = db.query(models.Contact).filter(
        models.Contact.first_response_time.isnot(None)
    ).all()
    
    avg_response_time = 0
    if contacted_leads:
        total_minutes = sum(
            (l.first_response_time - l.created_at).total_seconds() / 60.0
            for l in contacted_leads
        )
        avg_response_time = round(total_minutes / len(contacted_leads), 1)
        
    # Escalated Leads
    escalated_leads = db.query(models.ActionLog).filter(
        models.ActionLog.action_type == "Escalation"
    ).count()
    
    return {
        "total_leads_today": total_leads_today,
        "high_priority_leads": high_priority_leads,
        "avg_response_time_mins": avg_response_time,
        "escalation_count": escalated_leads
    }
