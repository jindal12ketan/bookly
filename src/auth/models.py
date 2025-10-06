from sqlmodel import Field, SQLModel, Relationship
import uuid
from datetime import datetime
from sqlalchemy import Column, text
import sqlalchemy.dialects.postgresql as pg
from typing import List
from src.books import models


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
    books: List["models.Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )  # Establish relationship with Book model
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
