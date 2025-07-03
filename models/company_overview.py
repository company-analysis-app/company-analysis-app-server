from sqlalchemy import Column, Text, TIMESTAMP, Integer
from sqlalchemy.dialects.mysql import VARCHAR
from database import Base

class CompanyOverviews(Base):
    __tablename__ = "company_overview"
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci'
    }

    corp_code = Column(VARCHAR(8), primary_key=True)
    corp_name = Column(VARCHAR(255))
    stock_code = Column(VARCHAR(10))
    ceo_nm = Column(VARCHAR(255))
    corp_cls = Column(VARCHAR(10))
    jurir_no = Column(VARCHAR(20))
    bizr_no = Column(VARCHAR(20))
    adres = Column(Text)
    hm_url = Column(Text)
    ir_url = Column(Text)
    phn_no = Column(VARCHAR(50))
    fax_no = Column(VARCHAR(50))
    induty_code = Column(VARCHAR(20))
    induty_name = Column(VARCHAR(255))
    est_dt = Column(VARCHAR(8))
    acc_mt = Column(VARCHAR(2))
    modified_at = Column(TIMESTAMP)
    favorite_count = Column(Integer, default=0)