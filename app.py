from fastapi import FastAPI
from controller.controller import router as user_router

app = FastAPI(title="User Data API")

app.include_router(user_router, prefix="/users")
