from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from models.dart import Darts
from models.company_overview import CompanyOverviews
from database import get_db
import os


DART_API = os.getenv("dart_api_key")

router = APIRouter()

@router.get("/")
def get_bords(keyword: str, db: Session=Depends(get_db)):
    darts = db.query(
        Darts.corp_code,
        Darts.corp_name,
    ).filter(
        Darts.corp_name.ilike(f"%{keyword}%")
    ).order_by(
        Darts.corp_name.asc()
    ).all()

    if darts is None:
        return {"message": "해당 회사명을 찾을 수 없습니다."}
    
    result_list = []
    for row in darts:
        result_list.append({
            "corp_code": row.corp_code,
            "corp_name": row.corp_name
        })

    return result_list


# @router.get("/getInfos")
# def get_infos(code: str, db:Session=Depends(get_db)):
#     result = db.query(CompanyOverviews).filter(CompanyOverviews.corp_code == code).first()
#     return result

