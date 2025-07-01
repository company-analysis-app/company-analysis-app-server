import os
from httpx import AsyncClient

GROQ_API_URL = "https://api.groq.com/v1/summarize"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def summarize(company: str, financial_text: str, news_text: str) -> str:
    prompt = (
        f"회사명: {company}\n"
        f"재무정보 요약:\n{financial_text}\n\n"
        f"최신 뉴스:\n{news_text}\n\n"
        "위 내용을 종합하여 3~5문장으로 핵심 요약문을 작성해주세요."
    )
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    async with AsyncClient() as client:
        resp = await client.post(
            GROQ_API_URL,
            json={"prompt": prompt, "model": "groq-llama2"},
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("summary", "")
