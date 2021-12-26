from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint


# Schema for user
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    pass


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Schema for vote
class Vote(BaseModel):
    post_id: int
    vote_dir: conint(le=1)


# Schema for post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int


# Schema for token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
