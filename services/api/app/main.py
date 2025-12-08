from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.routes import health, generate_meme, jobs, upload, moment
from app.services.db import connect_db, disconnect_db

app = FastAPI(
    title="MemeMind API",
    version="0.1.0",
    description="Backend for MemeMind - AI Meme Generation Platform"
)

app.include_router(health.router)
app.include_router(generate_meme.router)
app.include_router(jobs.router)
app.include_router(upload.router, tags=["Upload"])
app.include_router(moment.router)

app.mount("/uploads", StaticFiles(directory="static/uploads"), name="uploads")

@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

@app.get("/")
async def root():
    return {"message": "Welcome to MemeMind API"}
