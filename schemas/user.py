from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    oauth_provider: str
    oauth_sub: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
