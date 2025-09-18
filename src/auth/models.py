from sqlmodel import Field, SQLModel
import uuid
from datetime import datetime
from sqlalchemy import Column, text
import sqlalchemy.dialects.postgresql as pg


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
    is_verified: bool = Field(default=False)
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
