from sqlalchemy import Column, Text, TIMESTAMP, Integer
from sqlalchemy.dialects.mysql import VARCHAR
from database import Base


class IndustryFavorite(Base):
    __tablename__ = "user_industry_favorite"
    __table_args__ = {"mysql_charset": "utf8", "mysql_collate": "utf8_general_ci"}

    user_id = Column(int, primary_key=True)
    industry_id = Column(int, primary_key=True)
