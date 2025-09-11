from sqlmodel import SQLModel, Field
from sqlalchemy import Column, text
import uuid
from datetime import datetime, date
import sqlalchemy.dialects.postgresql as pg

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
