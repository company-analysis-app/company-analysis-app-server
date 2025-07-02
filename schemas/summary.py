from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Dict, List


class SummaryBase(BaseModel):
    company_name: str


class SummaryCreate(SummaryBase):
    summary_text: str


class NewsArticle(BaseModel):
    id: str
    title: str
    link: HttpUrl  # 기존 url → link로 이름 변경
    pubDate: datetime  # string 형태로 와도 자동 파싱됨


class FinancialRecord(BaseModel):
    year: str = Field(..., description="연도 (예: '2022')")
    revenue: int = Field(..., description="매출 (단위: 원)")
    operatingProfit: int = Field(..., description="영업이익 (단위: 원)")
    netIncome: int = Field(..., description="당기순이익 (단위: 원)")


class SummaryRequest(BaseModel):
    company_name: str = Field(..., description="기업 이름")
    financial: List[FinancialRecord]  # ex: [{"year": "2022", "revenue": 1000000, "operatingProfit": 200000, "netIncome": 150000}, ...]
    news: Dict[str, List[NewsArticle]]  # ex: {"전체": [{"id": "1", "title": "뉴스 제목", "link": "https://example.com/news1", "pubDate": "2023-10-01T12:00:00"}]}


class SummaryOut(SummaryBase):
    id: int
    summary_text: str
    created_at: datetime
    updated_at: datetime  # ← 추가

    class Config:
        orm_mode = True
