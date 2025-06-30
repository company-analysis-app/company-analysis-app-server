from fastapi import FastAPI, Request, Response
from routers import auth, users, dart
from database import Base, engine
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv(override=True)  # .env 파일 읽기(덮어쓰기 허용)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3000/",      # 슬래시 포함
    "http://127.0.0.1:3000",      
    "http://127.0.0.1:3000/",      
]

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 특정 출처의 도메인을 허용
    allow_credentials=True,  # 로그인 세션유지, 인증 토큰 사용 시 true
    allow_methods=["*"],  # GET, PUT, POST, DELETE
    allow_headers=["*"],  # 대표적인 예) Authorization, X-Custom-Header
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(dart.router, prefix='/darts', tags=["Darts"])
