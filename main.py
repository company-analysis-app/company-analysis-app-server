from fastapi import FastAPI, Request, Response
from routers import auth, users, dart, naver_news
from database import Base, engine
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv(override=True)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3000/",
    "http://127.0.0.1:3000",      
    "http://127.0.0.1:3000/",      
]
app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(naver_news.router, prefix="/naver", tags=["Naver News"])