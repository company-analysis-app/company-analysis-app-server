from fastapi import APIRouter

router = APIRouter()


@router.get("/login/google")
def login_google():
    return {"msg": "구글 OAuth 시작"}  # OAuth 구현 필요


@router.get("/callback/google")
def callback_google():
    return {"msg": "구글 OAuth 콜백"}  # OAuth 구현 필요
