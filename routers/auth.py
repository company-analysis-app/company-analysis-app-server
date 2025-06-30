# /routers/auth.py
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request, HTTPException, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os
from datetime import datetime, timedelta
import jwt
from database import get_db  # DB 세션 의존성
from models.user import User



router = APIRouter(tags=["auth"])

SECRET = os.getenv("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/google")

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)  # 구글 OAuth2 클라이언트 등록 :contentReference[oaicite:1]{index=1}

@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for("auth_callback_google")
    return await oauth.google.authorize_redirect(request, redirect_uri)


def create_access_token(data: dict, expires_seconds: int = 3600):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(seconds=expires_seconds)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm="HS256")


@router.get("/callback/google", name="auth_callback_google")
async def auth_callback_google(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    if not user_info or "email" not in user_info:
        raise HTTPException(status_code=400, detail="구글 사용자 정보 조회 실패")
    # 1) DB에서 사용자 조회 또는 신규 생성
    user = (
        db.query(User)
        .filter_by(oauth_provider="google", oauth_sub=user_info["sub"])
        .first()
    )
    if not user:
        user = User(
            email=user_info["email"],
            name=user_info.get("name"),
            oauth_provider="google",
            oauth_sub=user_info["sub"],
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    # 2) JWT 발급
    access_token = create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user_id = payload.get("user_id")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다")
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user