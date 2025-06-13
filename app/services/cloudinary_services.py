from fastapi import FastAPI, File, UploadFile, HTTPException
import cloudinary
import cloudinary.uploader
from app.config.env_secrets import get_env_variable

cloudinary.config(
    cloud_name= get_env_variable("CLOUDINARY_CLOUD_NAME"),
    api_key= get_env_variable("CLOUDINARY_API_KEY"),
    api_secret= get_env_variable("CLOUDINARY_API_SECRET"),
)

async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        upload_result = cloudinary.uploader.upload(
           contents,
           resource_type="auto"
        )
        return {"message": "File uploaded successfully", "url": upload_result["secure_url"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
       await file.close()