from pydantic import BaseModel
from fastapi import Query, Response, HTTPException, status
from app.services.user_services import check_if_exists, create_user
from app.services.jwt_services import create_jwt_token
from app.services.password_services import hash_password, verify_password

class User(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

async def user_creator(user: User, response: Response):
    email = user.email
    existing_user = await check_if_exists(email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    hashed_password = hash_password(user.password)
    user.password = hashed_password
    user = await create_user(user)

    token = create_jwt_token(user.email)
    response.set_cookie(key="access_token", value=token, httponly=True)

    return {
        "message": "User created successfully",
        "user": user,
        "token": token
    }

async def user_login(user: UserLogin, response: Response):
    email = user.email
    existing_user = await check_if_exists(email)

    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email does not exist"
        )

    if not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    token = create_jwt_token(existing_user.email)
    response.set_cookie(key="access_token", value=token, httponly=True)

    return {
        "message": "Login successful",
        "user": existing_user,
        "token": token
    }

def user_logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}

