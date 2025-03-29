from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

# MongoDB Connection
MONGO_URL = "mongodb+srv://code_god:1MHwEGptmYQF1Grh@aoristai.1ofe1s4.mongodb.net/?retryWrites=true&w=majority&appName=AoristAI"
client = AsyncIOMotorClient(MONGO_URL)

@router.get("/health/mongodb", tags=["health"])
async def mongodb_health_check():
    try:
        # Ping the MongoDB server
        await client.admin.command("ping")
        return {"status": "healthy", "message": "MongoDB is up and running"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB Health Check Failed: {str(e)}")
