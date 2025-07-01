from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.groq_service import summarize
from services.summary_crud import (
    create_summary,
    get_recent_summary,
    update_summary
)
from schemas.summary import SummaryCreate, SummaryOut, SummaryRequest, NewsArticle
from typing import Dict, List

router = APIRouter(tags=["Summary"])


@router.post("", response_model=SummaryOut)
async def summarize_with_client_data(
    req: SummaryRequest,
    db: Session = Depends(get_db)
):
    # 1) 이미 저장된 요약이 있는지 확인
    existing = get_recent_summary(db, req.company_name)

    # 2) 전달받은 JSON → 텍스트 포맷 변환
    def format_financial(f: Dict[str, Dict]) -> str:
        return "\n".join(
            f"{year}년 매출액 {vals['매출액']}원, 영업이익 {vals['영업이익']}원"
            for year, vals in f.items()
        )

    def format_news(articles: List[NewsArticle]) -> str:
        return "\n".join(
            f"{a.title} ({a.pubDate}) - {a.url}"
            for a in articles
        )

    fin_text = format_financial(req.financial)
    news_text = format_news(req.news["articles"])

    # 3) Groq 요약 호출
    try:
        summary_text = await summarize(req.company_name, fin_text, news_text)
    except Exception:
        raise HTTPException(502, detail="Groq 요약 서비스 오류")

    # 4) SummaryCreate 스키마로 데이터 준비
    summary_data = SummaryCreate(
        company_name=req.company_name,
        summary_text=summary_text
    )

    # 5) Upsert: 업데이트할 레코드가 있으면 update, 없으면 create
    if existing:
        updated = update_summary(db, req.company_name, summary_text)
        if updated:
            return updated
        # (혹시 update 실패 시) 새로 생성
        return create_summary(db, summary_data)
    else:
        return create_summary(db, summary_data)