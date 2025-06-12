from pydantic import BaseModel
from fastapi import Query
from app.services.user_services import check_if_exists

class User(BaseModel):
    username: str
    email: str
    password: str

async def user_creator(user: User):
    """Creates new user if there is no one with same email"""
    email = user.email
    existing_user = check_if_exists(email)
    if existing_user is not None:
        return {"error": "User with this email already exists"}
    
    return {"message": "User created successfully", "user": user}
