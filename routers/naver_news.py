# routers/naver_news.py
from fastapi import APIRouter, Query
from typing import List
import httpx
import os
import html


router = APIRouter()

@router.get("/news")
async def get_news(query: str = Query(...)):
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError("환경변수 NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET가 설정되지 않았습니다.")

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=5&sort=sim"

    print("요청 URL:", url)
    print("헤더:", headers)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        print("응답 상태 코드:", response.status_code)
        print("응답 내용:", response.text)
        response.raise_for_status()

        result = response.json()

        articles = [
            { 
                "title": html.unescape(item["title"].replace("<b>", "").replace("</b>", "")),
                "url": item["link"],
                "url": item["link"],
                "pubDate": item["pubDate"]
            }
            for item in result.get("items", [])
        ]

        return {"articles": articles}


