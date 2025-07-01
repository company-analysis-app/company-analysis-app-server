from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.dart_service import get_financial_text  # 이미 구현된 DART 서비스
from services.news_service import get_news_text      # 이미 구현된 네이버 뉴스 서비스
from services.groq_service import summarize
from services.summary_crud import create_summary, get_recent_summary
from schemas.summary import SummaryOut

router = APIRouter(tags=["Summary"])

@router.get("/{company_name}", response_model=SummaryOut)
async def get_summary(company_name: str, db: Session = Depends(get_db)):
    # 1) 캐시된 요약 확인
    cached = get_recent_summary(db, company_name)
    if cached:
        return cached

    # 2) DART 재무정보, 뉴스 가져오기
    financial = await get_financial_text(company_name)
    news = await get_news_text(company_name)

    # 3) Groq 요약
    try:
        summary_text = await summarize(company_name, financial, news)
    except Exception as e:
        raise HTTPException(502, detail="Groq 요약 서비스 오류")

    # 4) DB 저장 후 반환
    new_summary = create_summary(db, {"company_name": company_name, "summary_text": summary_text})
    return new_summary
