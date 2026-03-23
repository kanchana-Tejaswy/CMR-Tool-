from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
import json
import urllib.request
import urllib.error

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/leads",
    tags=["leads"],
)

WEBHOOK_URL = "http://localhost:5678/webhook/inbound-lead"

def trigger_webhook(lead_data: dict):
    req = urllib.request.Request(WEBHOOK_URL, method="POST")
    req.add_header("Content-Type", "application/json")
    data = json.dumps(lead_data).encode("utf-8")
    try:
        urllib.request.urlopen(req, data=data, timeout=5)
    except Exception as e:
        print(f"Webhook failed: {e}")

@router.get("", response_model=list[schemas.Lead])
def get_leads(db: Session = Depends(get_db)):
    return db.query(models.Lead).order_by(models.Lead.created_at.desc()).all()

@router.post("", response_model=schemas.Lead)
def create_lead(lead_in: schemas.LeadCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_lead = db.query(models.Lead).filter(models.Lead.email == lead_in.email).first()
    if db_lead:
        raise HTTPException(status_code=400, detail="Lead already exists")
    
    new_lead = models.Lead(
        name=lead_in.name,
        email=lead_in.email,
        phone=lead_in.phone,
        company=lead_in.company,
        lead_source=lead_in.lead_source,
        status="new"
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    
    # Notify webhook
    webhook_payload = {
        "lead_id": new_lead.id,
        "name": new_lead.name,
        "email": new_lead.email,
        "company": new_lead.company,
        "phone": new_lead.phone,
        "lead_source": new_lead.lead_source
    }
    background_tasks.add_task(trigger_webhook, webhook_payload)
    
    return new_lead

@router.patch("/{lead_id}", response_model=schemas.Lead)
def update_lead(lead_id: int, lead_update: schemas.LeadUpdate, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    if lead_update.ai_priority is not None:
        lead.ai_priority = lead_update.ai_priority
    if lead_update.ai_score is not None:
        lead.ai_score = lead_update.ai_score
    if lead_update.ai_next_action is not None:
        lead.ai_next_action = lead_update.ai_next_action
    if lead_update.status is not None:
        lead.status = lead_update.status
        
    db.commit()
    db.refresh(lead)
    return lead

