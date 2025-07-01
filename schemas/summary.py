from pydantic import BaseModel
from datetime import datetime

class SummaryBase(BaseModel):
    company_name: str

class SummaryCreate(SummaryBase):
    summary_text: str

class SummaryOut(SummaryBase):
    id: int
    summary_text: str
    created_at: datetime

    class Config:
        orm_mode = True
