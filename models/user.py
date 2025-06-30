from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
        "mysql_collate": "utf8_general_ci",
    }

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(100))
    oauth_provider = Column(String(50))
    oauth_sub = Column(String(100))
