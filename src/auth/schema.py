from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import List
from src.books.schema import Book


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=20)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    password_hash: str
    first_name: str
    last_name: str
    role: str
    is_verified: bool = Field(default=False)
    created_at: datetime
    updated_at: datetime


class UserBooksModel(UserModel):
    books: List[Book]


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
