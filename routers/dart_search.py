from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from models.company_overview import CompanyOverviews
from database import get_db
from services import logo_api

router = APIRouter()


@router.post("/")
def get_bords(keyword: str, db: Session = Depends(get_db)):
    companies = (
        db.query(CompanyOverviews)
        .filter(CompanyOverviews.corp_name.ilike(f"%{keyword}%"))
        .order_by(CompanyOverviews.corp_name.asc())
        .all()
    )

    if companies is None:
        raise HTTPException(status_code=404, detail="회사를 찾을 수 없습니다.")

    result_list = []

    for comp in companies:
        # 2) logo가 비어 있고, hm_url이 있으면 API 호출
        if comp.logo == "" and comp.hm_url:
            try:
                logo_url = logo_api.fetch_logo_url(comp.hm_url)
                if logo_url:
                    comp.logo = logo_url
                    db.add(comp)
                    db.commit()
                    db.refresh(comp)
            except Exception as e:
                # 로깅 또는 무시
                print(f"[logo_api error] {comp.corp_code}: {e}")

        # 3) logo != '' 이거나(이미 채워짐) hm_url도 없으면 그냥 건너뜀

        result_list.append(
            {
                "corp_code": comp.corp_code,
                "corp_name": comp.corp_name,
                "hm_url": comp.hm_url,
                "logo": comp.logo,
            }
        )

    return result_list


@router.get("/bestCompanies")
def get_best_companies(db: Session = Depends(get_db)):
    best_results = (
        db.query(
            CompanyOverviews.corp_code,
            CompanyOverviews.corp_name,
            CompanyOverviews.favorite_count,
        )
        .order_by(CompanyOverviews.favorite_count.desc())
        .limit(3)
        .all()
    )

    if not best_results:
        return {"message": "해당 회사명을 찾을 수 없습니다."}

    result_list = []
    for row in best_results:
        result_list.append(
            {
                "corp_code": row.corp_code,
                "corp_name": row.corp_name,
                "favorite_count": row.favorite_count,
            }
        )

    return result_list
