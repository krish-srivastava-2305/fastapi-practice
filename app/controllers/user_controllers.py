from pydantic import BaseModel
from fastapi import Query, Response
from app.services.user_services import check_if_exists, create_user
from app.services.jwt_services import create_jwt_token
from app.services.password_services import hash_password

class User(BaseModel):
    username: str
    email: str
    password: str

async def user_creator(user: User, response: Response):
    """Creates new user if there is no one with same email"""
    email = user.email
    existing_user = await check_if_exists(email)
    print(f"Checking if user with email {email} exists: {existing_user}")
    if existing_user is not None:
        return {"error": "User with this email already exists"}
    
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    print(f"Creating user with email: {user.email} and hashed password: {user.password}")
    user = await create_user(user)
    print(f"User created: {user}")

    token = create_jwt_token(user.email)

    # Set cookie
    response.set_cookie(key="access_token", value=token, httponly=True)

    return {
        "message": "User created successfully",
        "user": user,
        "token": token
    }
