from fastapi import Depends
from sqlalchemy.orm import Session
from models.summary import Summary
from schemas.summary import SummaryCreate
from database import get_db

def create_summary(data: SummaryCreate, db: Session = Depends(get_db)) -> Summary:
    db_obj = Summary(**data.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_recent_summary(db: Session, company: str):
    return (
        db.query(Summary)
        .filter(Summary.company_name == company)
        .order_by(Summary.created_at.desc())
        .first()
    )
