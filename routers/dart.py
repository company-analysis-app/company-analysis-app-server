from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from models.dart import Darts
from models.company_overview import CompanyOverviews
from database import get_db
import os
import requests as rq
import pandas as pd



DART_API = os.getenv("dart_api_key")

router = APIRouter()

@router.get("/getInfos")
def get_company_info(name: str, db: Session = Depends(get_db)):
    result = (
        db.query(
            Darts.corp_code,
            Darts.corp_name,
            CompanyOverviews.adres,
            CompanyOverviews.corp_cls,
            CompanyOverviews.est_dt,
            CompanyOverviews.hm_url,
            CompanyOverviews.induty_name
        )
        .join(CompanyOverviews, Darts.corp_code == CompanyOverviews.corp_code)
        .filter(Darts.corp_name == name)
        .first()
    )

    if result is None:
        return {"message": "해당 회사명을 찾을 수 없습니다."}

    final_result = {
        "corp_code": result.corp_code,
        "corp_name": result.corp_name,
        "adres": result.adres,
        "corp_cls": result.corp_cls,
        "est_dt": result.est_dt,
        "hm_url": result.hm_url,
        "induty_name": result.induty_name,
    }

    return final_result



@router.get("/getValues")
def get_values(code: str):
    url = f"https://opendart.fss.or.kr/api/fnlttSinglAcnt.json?crtfc_key={DART_API}&corp_code={code}&bsns_year=2024&reprt_code=11011"
    response = rq.get(url)
    data = response.json()

    if 'list' not in data:
        return {"message": "데이터가 없습니다."}

    df = pd.DataFrame(data['list'])
    df_cfs = df[df['fs_div'] == 'CFS']

    keywords = ['매출액', '영업이익', '당기순이익', '자본총계']
    df_filtered = df_cfs[df_cfs['account_nm'].apply(lambda x: any(k in x for k in keywords))]

    def clean(val):
        return int(val.replace(",", "")) if isinstance(val, str) and val else None

    result = {
        "2022": {},
        "2023": {},
        "2024": {}
    }

    def normalize(name):
        return name.split("(")[0].strip()

    for _, row in df_filtered.iterrows():
        account = normalize(row['account_nm'])
        result['2022'][account] = clean(row.get('bfefrmtrm_amount'))
        result['2023'][account] = clean(row.get('frmtrm_amount'))
        result['2024'][account] = clean(row.get('thstrm_amount'))

    def calculate_ratios(year):
        res = result[year]
        sales = res.get('매출액')
        op = res.get('영업이익')
        net = res.get('당기순이익')
        equity = res.get('자본총계')

        ratios = {}
        if sales and sales != 0:
            ratios['영업이익률'] = round(op / sales * 100, 2) if op else None
            ratios['순이익률'] = round(net / sales * 100, 2) if net else None
        if equity and equity != 0:
            ratios['ROE'] = round(net / equity * 100, 2) if net else None
        return ratios
    

    for year in ['2022', '2023', '2024']:
        result[year]['ratio'] = calculate_ratios(year)

    return result



@router.post("/company/addfavorites/{corp_code}")
def add_favorites(corp_code: int, db: Session = Depends(get_db)):
    data = db.query(CompanyOverviews).filter(CompanyOverviews.corp_code == corp_code).first()
    if not data:
        raise HTTPException(status_code=404, detail="해당 기업을 찾을 수 없습니다.")
    
    data.favorite_count += 1
    db.commit()
    db.refresh(data)
    return {"favorite_count": data.favorite_count}


@router.post("/company/subfavorites/{corp_code}")
def sub_favorites(corp_code: int, db: Session = Depends(get_db)):
    data = db.query(CompanyOverviews).filter(CompanyOverviews.corp_code == corp_code).first()
    if not data:
        raise HTTPException(status_code=404, detail="해당 기업을 찾을 수 없습니다.")
    
    if data.favorite_count > 0:
        data.favorite_count -= 1
        db.commit()
        db.refresh(data)
    
    return {"favorite_count": data.favorite_count}