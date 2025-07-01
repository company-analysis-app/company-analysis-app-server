from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

# .env 파일 로딩
load_dotenv()

# os.getenv를 통한 확인
database_url = os.getenv("DATABASE_URL")
print("os.getenv:", database_url)

# Pydantic Settings 클래스 정의
class Settings(BaseSettings):
    database_url: str
    debug: bool = False  # 기본값 가능

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# settings 인스턴스 생성
settings = Settings()

# Pydantic 방식으로 확인
print("pydantic settings:", settings.database_url)
