from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from models.dart import Darts
from database import get_db
import os
import requests as rq
import pandas as pd


DART_API = os.getenv("dart_api_key")

router = APIRouter()

@router.get("/")
def get_bords(name: str, db: Session=Depends(get_db)):
    darts = db.query(
        Darts.corp_code,
    ).filter(Darts.corp_name == name).first()

    if darts is None:
        return {"message": "해당 회사명을 찾을 수 없습니다."}

    return darts[0]

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


@router.get("/getInfos")
def get_indu_code(code: str):
   url = f"https://opendart.fss.or.kr/api/company.json?crtfc_key={DART_API}&corp_code={code}"
   data = rq.get(url)
   result = data.json()
   return result


@router.get("/mapping")
def code_mapping(code: int):
   df = pd.read_csv('산업코드.csv')
   match = df[df['산업코드'] == code]
   if match.empty:
        raise HTTPException(status_code=404, detail="해당 코드를 찾을 수 없습니다.")
   return match["산업코드명"].iloc[0]

