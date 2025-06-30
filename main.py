from fastapi import FastAPI
from routers import auth #, companies, users, recommendations
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(naver_news.router)
# app.include_router(companies.router, prefix="/companies", tags=["Companies"])
# app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
