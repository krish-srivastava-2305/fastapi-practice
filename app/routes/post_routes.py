from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, Request
from typing import Optional

post_router = APIRouter(prefix="/api/v1/posts", tags=["posts"])

from app.controllers.post_controllers import create_post

@post_router.post("/", response_model=dict)
async def create_post_route(
    request: Request,
    title: str = Form(..., min_length=1, max_length=100),
    content: Optional[str] = Form(None),
    media_file: Optional[UploadFile] = File(None)
):
    post_data = {
        "title": title,
        "content": content,
        "media_file": media_file
    }
    token = request.cookies.get("access_token")
    created_post = await create_post(post_data, token)
    if not created_post:
        raise HTTPException(status_code=400, detail="Post creation failed")
    return created_post
