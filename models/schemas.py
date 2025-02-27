from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserLogin(UserBase):
    password: str = Field(...)

class Token(BaseModel):
    token: str

class PostBase(BaseModel):
    text: str = Field(..., max_length=1048576)  # 1MB in characters

    @validator('text')
    def validate_size(cls, v):
        """Validate payload size doesn't exceed 1MB"""
        if len(v.encode('utf-8')) > 1048576:
            raise ValueError('Post size exceeds 1MB')
        return v

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True