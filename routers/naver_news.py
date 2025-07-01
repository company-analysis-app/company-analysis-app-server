# routers/naver_news.py
from fastapi import APIRouter, Query
from typing import List
import httpx
import os
import html
import asyncio


router = APIRouter()
CATEGORIES = ["전체", "채용", "주가", "노사", "IT"]

async def fetch_news(query):
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET 환경변수가 없습니다.")
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=5&sort=sim"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        try:
            result = response.json()
        except Exception:
            # 응답이 JSON이 아니면 에러 메시지와 함께 예외 발생
            print("응답이 JSON이 아님:", response.text[:500])
            raise RuntimeError(f"네이버 API에서 JSON이 아닌 응답을 받았습니다. (query={query})")
        articles = [
            {
                "title": html.unescape(item["title"].replace("<b>", "").replace("</b>", "")),
                "url": item["link"],
                "pubDate": item["pubDate"]
            }
            for item in result.get("items", [])
        ]
        return articles

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
                "pubDate": item["pubDate"]
            }
            for item in result.get("items", [])
        ]

        return {"articles": articles}

@router.get("/news/all")
async def get_all_news(company: str = Query(...)):
    tasks = []
    for cat in CATEGORIES:
        if cat == "전체":
            q = company
        else:
            q = f"{company} {cat}"
        tasks.append(fetch_news(q))
    results = await asyncio.gather(*tasks)
    return {cat: news for cat, news in zip(CATEGORIES, results)}


