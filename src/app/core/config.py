from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Management API"
    client = AsyncIOMotorClient("mongodb+srv://code_god:1MHwEGptmYQF1Grh@aoristai.1ofe1s4.mongodb.net/?retryWrites=true&w=majority&appName=AoristAI")
    db = client["agora_vission"]
    collection = db["viewer_data"]
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Add OAuth2 scheme for token authentication
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

    class Config:
        env_file = ".env.local"

settings = Settings()