from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import VARCHAR
from database import Base


class IndustryFavorite(Base):
    __tablename__ = "user_industry_favorite"
    __table_args__ = {"mysql_charset": "utf8", "mysql_collate": "utf8_general_ci"}

    user_id = Column(Integer, primary_key=True)
    industry_id = Column(Integer, primary_key=True)
