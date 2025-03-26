from fastapi import APIRouter, WebSocket
import asyncio
import datetime
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

MONGO_URI = "mongodb+srv://code_god:1MHwEGptmYQF1Grh@aoristai.1ofe1s4.mongodb.net/?retryWrites=true&w=majority&appName=AoristAI"

client = AsyncIOMotorClient(MONGO_URI)
db = client["marketing_insights"]
collection = db["viewer_data"]

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Send real-time updates over WebSockets"""
    await websocket.accept()
    while True:
        latest = await collection.find().sort("_id", -1).limit(1).to_list(length=1)
        if latest:
            latest[0].pop("_id", None)  # Remove `_id` field
            await websocket.send_json(latest[0])
        await asyncio.sleep(2)

@router.get("/insights")
async def get_insights():
    """Fetch all logged insights"""
    insights = await collection.find().to_list(None)  # Fetch all insights
    for doc in insights:
        doc.pop("_id", None)  # Remove `_id` field
    return {
        "status": "success",
        "data": insights
    }

@router.get("/insights/count")
async def count():
    """Count insights based on gender"""
    male_count = await collection.count_documents({"gender": "Male"})
    female_count = await collection.count_documents({"gender": "Female"})

    return {
        "status": "success",
        "counts": {
            "male": male_count,
            "female": female_count
        }
    }
