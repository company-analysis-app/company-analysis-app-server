from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.user import User as UserModel, IndustryClassification, UserIndustryFavorite
from schemas.user import PreferencesUpdate, FavoriteCreate, UserOut, IndustryCategoryNode
from routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(tags=["Users"])

def user_out_safe(user: UserModel) -> UserOut:
    return UserOut(
        id=getattr(user, 'id'),
        email=getattr(user, 'email'),
        name=getattr(user, 'name'),
        oauth_provider=getattr(user, 'oauth_provider'),
        oauth_sub=getattr(user, 'oauth_sub'),
        preferences=list(getattr(user, 'preferences') or []),
        favorites=list(getattr(user, 'favorites') or []),
        created_at=getattr(user, 'created_at'),
        updated_at=getattr(user, 'updated_at'),
    )

# 1) 현재 사용자 정보 조회
@router.get("/me", response_model=UserOut)
def read_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


# 2) 선호 카테고리 업데이트
@router.put("/preferences", response_model=UserOut)
def update_preferences(
    prefs: PreferencesUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.preferences is None:
        current_user.preferences = []
    else:
        current_user.preferences.clear()
    current_user.preferences.extend(prefs.preferences)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


# 3) 관심기업 추가
@router.post("/favorites", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def add_favorite(
    fav: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if fav.company_id not in current_user.favorites:
        current_user.favorites.append(fav.company_id)
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
    return current_user


# 4) 관심기업 제거
@router.delete("/favorites/{company_id}", response_model=UserOut)
def remove_favorite(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if company_id in current_user.favorites:
        current_user.favorites.remove(company_id)
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
    return current_user

# 5) 산업군 목록 조회
@router.get("/industries", response_model=List[IndustryCategoryNode])
def get_industries(db: Session = Depends(get_db)):
    industries = db.query(IndustryClassification).all()
    return [IndustryCategoryNode.from_orm(ind) for ind in industries]

class IndustryFavoriteCreate(BaseModel):
    industry_id: int

# 6) 관심 산업군 추가
@router.post("/industry-favorites", response_model=List[int])
def add_industry_favorites(
    industry_ids: List[int],
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    for industry_id in industry_ids:
        exists = db.query(UserIndustryFavorite).filter_by(
            user_id=current_user.id, industry_id=industry_id
        ).first()
        if not exists:
            db.add(UserIndustryFavorite(user_id=current_user.id, industry_id=industry_id))
    db.commit()
    rows = db.query(UserIndustryFavorite).filter_by(user_id=current_user.id).all()
    return [row.industry_id for row in rows]

# 7) 관심 산업군 제거
@router.delete("/industry-favorites/{industry_id}", response_model=List[int])
def remove_industry_favorite(
    industry_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    row = db.query(UserIndustryFavorite).filter_by(
        user_id=current_user.id, industry_id=industry_id
    ).first()
    if row:
        db.delete(row)
        db.commit()
    rows = db.query(UserIndustryFavorite).filter_by(user_id=current_user.id).all()
    return [row.industry_id for row in rows]

@router.post("/users/industry-favorites")
def add_industry_favorite(code: str, db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)):
    # code가 일치하는 industry를 찾는다
    industry = db.query(IndustryClassification).filter(
        (IndustryClassification.code_2 == code) |
        (IndustryClassification.code_3 == code) |
        (IndustryClassification.code_4 == code) |
        (IndustryClassification.code_5 == code)
    ).first()

    if not industry:
        raise HTTPException(status_code=404, detail="해당 코드의 산업군이 존재하지 않습니다.")

    # 이미 등록되어 있으면 무시
    existing = db.query(UserIndustryFavorite).filter_by(
        user_id=user.id,
        industry_id=industry.id
    ).first()

    if existing:
        return {"message": "이미 등록된 관심 산업군입니다."}

    # 새로 추가
    favorite = UserIndustryFavorite(
        user_id=user.id,
        industry_id=industry.id
    )
    db.add(favorite)
    db.commit()

    return {"message": "관심 산업군 등록 완료"}

@router.get("/industry-favorites", response_model=List[int])
def get_industry_favorites(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    rows = db.query(UserIndustryFavorite).filter_by(user_id=current_user.id).all()
    return [row.industry_id for row in rows]