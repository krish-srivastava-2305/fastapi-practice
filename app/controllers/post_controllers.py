from typing import Annotated, Optional
from fastapi import HTTPException, Form, File, UploadFile
from pydantic import BaseModel
from app.services.post_services import post_creator
from app.services.cloudinary_services import upload_file
from app.services.jwt_services import decode_jwt_token

async def create_post(post: dict, token: str):
    try:
        media_url = None
        if post.get("media_file"):
            upload_result = await upload_file(post["media_file"])
            media_url = upload_result.get("url")
            if not media_url:
                raise HTTPException(status_code=400, detail="Media upload failed")
        
        decoded_token = decode_jwt_token(token)
        if not decoded_token:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        post_data = {
            "title": post["title"],
            "content": post.get("content", ""),
            "media_url": media_url,
            "author_id": decoded_token.get("sub")
        }
        # print(f"Creating post with data: {post_data}")
        created_post = await post_creator(post_data)
        if not created_post:
            raise HTTPException(status_code=400, detail="Post creation failed")
        return created_post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


