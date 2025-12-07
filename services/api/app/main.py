from fastapi import FastAPI
from app.routes import health, generate_meme, moment
from app.services import db

app = FastAPI(
    title="MemeMind API",
    version="0.1.0",
    description="Backend for MemeMind - AI Meme Generation Platform"
)

app.include_router(health.router)
app.include_router(generate_meme.router)
app.include_router(moment.router)

@app.on_event("startup")
async def startup():
    await db.connect_db()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect_db()

@app.get("/")
async def root():
    return {"message": "Welcome to MemeMind API"}
