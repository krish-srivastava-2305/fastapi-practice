from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.routes.user_routes import user_router
from app.routes.post_routes import post_router

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

allowed_origins = [
    "http://localhost:3000",
    "https://www.example.com",
    "https://your-production-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def read_root():
    return {"message": "Healthy!"}

app.include_router(user_router)
app.include_router(post_router)