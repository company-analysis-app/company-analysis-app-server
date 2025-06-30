from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.user import User as UserModel
from schemas.user import PreferencesUpdate, FavoriteCreate, UserOut
from routers.auth import get_current_user

router = APIRouter(tags=["Users"])


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
    current_user.preferences = prefs.preferences
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
