from sqlalchemy import Column, Integer, String, JSON, DateTime, UniqueConstraint
from database import Base
from datetime import datetime
import pytz


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("oauth_provider", "oauth_sub", name="uq_provider_sub"),
        {
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8mb4",
            "mysql_collate": "utf8mb4_unicode_ci",
        },
    )

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    oauth_provider = Column(String(50), nullable=False)
    oauth_sub = Column(String(100), nullable=False)

    # JSON 컬럼 기본값은 Python 레벨로 처리 (MySQL JSON 컬럼은 기본값 설정 불가)
    preferences = Column(JSON, nullable=False, default=list)
    favorites = Column(JSON, nullable=False, default=list)

    # 생성 시각 (한국 시간)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Asia/Seoul")),
        nullable=False,
    )
    # 수정 시각 (한국 시간)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Asia/Seoul")),
        onupdate=lambda: datetime.now(pytz.timezone("Asia/Seoul")),
        nullable=False,
    )
