from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth #, companies, users, recommendations
from database import Base, engine
from routers import naver_news


Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(naver_news.router, prefix="/naver", tags=["Naver News"])
# app.include_router(companies.router, prefix="/companies", tags=["Companies"])
# app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
