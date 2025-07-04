from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.user import User as UserModel, IndustryClassification
from schemas.user import PreferencesUpdate, UserOut, IndustryCategoryNode
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
    if current_user.preferences is not None:
        current_user.preferences.clear()
        current_user.preferences.extend(prefs.preferences)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


# 5) 산업군 목록 조회
@router.get("/industries", response_model=List[IndustryCategoryNode])
def get_industries(db: Session = Depends(get_db)):
    industries = db.query(IndustryClassification).all()
    return [IndustryCategoryNode.from_orm(ind) for ind in industries]
