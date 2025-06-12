from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Annotated
from app.controllers.user_controllers import user_creator

user_router = APIRouter(prefix="/api/v1/user", tags=["user"])

class User(BaseModel):
    username: Annotated[str, Query(min_length=3, max_length=50)]
    email: Annotated[str, Query(max_length=30)]
    password: Annotated[str, Query(min_length=6)]



@user_router.post("/register")
async def create_user(user: User):
    return await user_creator(user)
