# routers/dart_search.py
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from models.user_industry_favorite import IndustryFavorite
from models.industry_classification import IndustryClassification
from models.company_overview import CompanyOverviews
from database import get_db
from sqlalchemy.sql.expression import func
from services.logo_api import update_company_logo

router = APIRouter()


@router.get("/getIndustryCode")
def get_industry_code(user_id: int, db: Session = Depends(get_db)):
    favorite = (
        db.query(IndustryFavorite.industry_id)
        .filter(IndustryFavorite.user_id == user_id)
        .first()
    )

    if not favorite:
        raise HTTPException(status_code=404, detail="회사를 찾을 수 없습니다.")

    return favorite.industry_id



@router.get("/getData")
def get_data(industry_code: int, db: Session = Depends(get_db)):
    result = (
        db.query(CompanyOverviews)
        .filter(CompanyOverviews.induty_code == industry_code)
        .order_by(func.rand())
        .all()
    )

    if not result:
        raise HTTPException(status_code=404, detail="회사를 찾을 수 없습니다.")

    result_list = []
    for row in result:
        row.logo = update_company_logo(row, db)
        result_list.append({
            "corp_code": row.corp_code,
            "corp_name": row.corp_name,
            "induty_code": row.induty_code,
            "logo": row.logo,
        })

    return result_list


