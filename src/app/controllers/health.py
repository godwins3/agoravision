from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

# MongoDB Connection
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)

@router.get("/health/mongodb", tags=["health"])
async def mongodb_health_check():
    try:
        # Ping the MongoDB server
        await client.admin.command("ping")
        return {"status": "healthy", "message": "MongoDB is up and running"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB Health Check Failed: {str(e)}")
