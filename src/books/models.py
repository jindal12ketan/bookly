from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, text
import uuid
from src.auth import models
from datetime import datetime, date
import sqlalchemy.dialects.postgresql as pg
from typing import Optional

# Book model representing a book entity in the database

"""Here we have used server-side defaults for UUID and timestamps for better performance and consistency."""


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=text("gen_random_uuid()"),
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    user: Optional["models.User"] = Relationship(
        back_populates="books"
    )  # Relationship with User model
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            server_default=text("NOW()"),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            server_default=text("NOW()"),
            server_onupdate=text("NOW()"),
            nullable=False,
        )
    )

    def __repr__(self):
        return f"<Book(title={self.title})>"
