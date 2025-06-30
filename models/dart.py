from sqlalchemy import Column, BigInteger, Text
from database import Base

class Darts(Base):
    __tablename__ = "dart_code"
    __table_args__ = {
        'mysql_charset': 'utf8', 
        'mysql_collate': 'utf8_general_ci'
    }
    index = Column(BigInteger)
    corp_code = Column(Text, primary_key=True)
    corp_name = Column(Text, nullable=False)
    corp_eng_name = Column(Text, nullable=False)
    stock_code = Column(Text, nullable=False)
    modify_date = Column(Text, nullable=False)