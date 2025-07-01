from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.groq_service import summarize
from services.summary_crud import create_summary, get_recent_summary
from schemas.summary import SummaryOut, SummaryRequest, NewsArticle
from typing import Dict, List

router = APIRouter(tags=["Summary"])


@router.post("", response_model=SummaryOut)
async def summarize_with_client_data(
    req: SummaryRequest, db: Session = Depends(get_db)
):
    # 1) 캐시된 요약 확인
    cached = get_recent_summary(db, req.company_name)
    if cached:
        return cached

    # 2) financial 및 news 데이터를 문자열로 포맷
    #    예: "{year}: 매출액 {매출액}, 영업이익 {영업이익}\n..." :contentReference[oaicite:3]{index=3}
    def format_financial(f: Dict[str, Dict]) -> str:
        lines = []
        for year, vals in f.items():
            lines.append(
                f"{year}년 매출액 {vals['매출액']}원, 영업이익 {vals['영업이익']}원"
            )
        return "\n".join(lines)

    def format_news(articles: List[NewsArticle]) -> str:
        return "\n".join(f"{a.title} ({a.pubDate}) - {a.url}" for a in articles)

    fin_text = format_financial(req.financial)
    news_text = format_news(req.news["articles"])

    # 3) Groq 요약 호출
    try:
        summary_text = await summarize(req.company_name, fin_text, news_text)
    except Exception:
        raise HTTPException(502, detail="Groq 요약 서비스 오류")

    # 4) DB 저장 후 반환
    new_summary = create_summary(
        db, {"company_name": req.company_name, "summary_text": summary_text}
    )
    return new_summary
