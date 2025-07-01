from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List


class SummaryBase(BaseModel):
    company_name: str


class SummaryCreate(SummaryBase):
    summary_text: str


class NewsArticle(BaseModel):
    title: str
    url: str
    pubDate: str


class SummaryRequest(BaseModel):
    company_name: str = Field(..., description="기업 이름")
    financial: Dict[
        str, Dict
    ]  # ex: {"2022": {...}, "2023": {...}} 형태
    news: Dict[
        str, List[NewsArticle]
    ]  # ex: {"articles": [ {...}, {...} ]} 형태


class SummaryOut(SummaryBase):
    id: int
    summary_text: str
    created_at: datetime
    updated_at: datetime   # ← 추가

    class Config:
        orm_mode = True
