from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    oauth_provider: str
    oauth_sub: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
