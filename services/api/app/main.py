from fastapi import FastAPI
from app.routes import health, generate_meme, moment

app = FastAPI(
    title="MemeMind API",
    version="0.1.0",
    description="Backend for MemeMind - AI Meme Generation Platform"
)

app.include_router(health.router)
app.include_router(generate_meme.router)
app.include_router(moment.router)

@app.get("/")
async def root():
    return {"message": "Welcome to MemeMind API"}
