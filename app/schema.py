from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class BaseModel(SQLModel):
    id: Optional[int] = Field (default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True


class User(BaseModel, table=True):
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)

class Post(BaseModel, table=True):
    title: str = Field(index=True, nullable=False)
    content: Optional[str] = None
    media_url: Optional[str] = None

    author_id: int = Field(foreign_key="user.id", nullable=False)
    author: Optional[User] = Relationship(back_populates="posts")
