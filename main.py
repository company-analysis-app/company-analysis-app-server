from fastapi import FastAPI
from routers import auth
from database import Base, engine
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

load_dotenv(override=True)  # .env 파일 읽기(덮어쓰기 허용)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))
Base.metadata.create_all(bind=engine)



app.include_router(auth.router, prefix="/auth", tags=["Auth"])
