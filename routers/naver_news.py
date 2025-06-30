from fastapi import APIRouter

router = APIRouter()

@router.get("/naver-news")
def get_naver_news():
    return {"message": "네이버 뉴스 API 연동 테스트"}
