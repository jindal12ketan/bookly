from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, text
import sqlalchemy.dialects.postgresql as pg
from typing import List, Optional
from datetime import datetime, date
import uuid

# region User Model
# User model representing a user entity in the database

"""Here we have used server-side defaults for UUID and timestamps for better performance and consistency."""


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=text("gen_random_uuid()"),
        )
    )
    username: str
    email: str
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
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
        return f"<User(username={self.username}, email={self.email})>"


# end region


# region Book Model
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
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )
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


# end region

# region Review Model
# Review model representing a review entity in the database

"""Here we have used server-side defaults for UUID and timestamps for better performance and consistency."""


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=text("gen_random_uuid()"),
        )
    )
    rating: int = Field(ge=1, le=5)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")
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
        return f"<Reviews for {self.book_uid} by user {self.user_uid}>"


# end region
