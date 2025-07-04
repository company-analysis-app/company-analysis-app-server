from sqlalchemy import Column, Integer, String, JSON, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import pytz

SEOUL_TZ = pytz.timezone("Asia/Seoul")
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

    preferences    = Column(MutableList.as_mutable(JSON), default=list, nullable=False)
    favorites      = Column(MutableList.as_mutable(JSON), default=list, nullable=False)
    favorites_industries = relationship("UserIndustryFavorite", back_populates="user")

    # 생성 시각 (한국 시각)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(SEOUL_TZ),
        nullable=False,
    )
    # 수정 시각 (한국 시각)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(SEOUL_TZ),
        onupdate=lambda: datetime.now(SEOUL_TZ),
        nullable=False,
    )

#산업군 
class IndustryClassification(Base):
    __tablename__ = "industry_classification"
    id = Column(Integer, primary_key=True, index=True)
    name_1 = Column(String(100), nullable=True)
    name_2 = Column(String(100), nullable=True)
    name_3 = Column(String(100), nullable=True)
    name_4 = Column(String(100), nullable=True)
    name_5 = Column(String(200), nullable=True)

class UserIndustryFavorite(Base):
    __tablename__ = "user_industry_favorite"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # industry_id에는 code_2, code_3, code_4, code_5 등 사용자가 선택한 depth의 code 값만 저장됨
    industry_id = Column(Integer, ForeignKey("industry_classification.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint("user_id", "industry_id", name="uniq_user_industry"),)

    user = relationship("User", back_populates="favorites_industries")
    industry = relationship("IndustryClassification")