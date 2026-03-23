from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/deals",
    tags=["deals"],
)

@router.post("/", response_model=schemas.Deal)
def create_deal(deal: schemas.DealCreate, db: Session = Depends(get_db)):
    db_deal = models.Deal(**deal.model_dump())
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal

@router.get("/", response_model=List[schemas.Deal])
def read_deals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    deals = db.query(models.Deal).offset(skip).limit(limit).all()
    return deals

@router.get("/board")
def read_deals_for_board(db: Session = Depends(get_db)):
    deals = db.query(models.Deal).all()
    results = []
    for d in deals:
        contact_name = "Unknown"
        company = "Unknown"
        priority = "Low"
        sdr_name = "Unassigned"
        
        if d.contact:
            contact_name = f"{d.contact.first_name} {d.contact.last_name}".strip()
            company = d.contact.company or "Unknown"
            priority = d.contact.priority
            
        if d.assigned_sdr:
            sdr_name = d.assigned_sdr.name
            
        results.append({
            "id": d.id,
            "title": d.title,
            "value": d.value,
            "stage": d.stage,
            "contact_name": contact_name,
            "company": company,
            "priority": priority,
            "sdr_name": sdr_name
        })
    return results

@router.get("/{deal_id}", response_model=schemas.Deal)
def read_deal(deal_id: int, db: Session = Depends(get_db)):
    db_deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return db_deal

@router.patch("/{deal_id}/stage", response_model=schemas.Deal)
def update_deal_stage(deal_id: int, stage: str, db: Session = Depends(get_db)):
    db_deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    db_deal.stage = stage
    db.commit()
    db.refresh(db_deal)
    return db_deal

@router.delete("/{deal_id}")
def delete_deal(deal_id: int, db: Session = Depends(get_db)):
    db_deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    db.delete(db_deal)
    db.commit()
    return {"status": "ok"}
