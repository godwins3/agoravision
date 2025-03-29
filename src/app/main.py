
import asyncio
import datetime
from fastapi import FastAPI

# from .services.utils.utils import analyze_frame 
from fastapi.middleware.cors import CORSMiddleware
from .controllers import health, stream # , auth

app = FastAPI(title="Real-Time Marketing Insights")


# Allow requests from your frontend (adjust as needed)
origins = [
    "http://localhost:3000",  # Your Next.js frontend
    "https://yourfrontend.com"  # Production frontend (optional)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins
    allow_credentials=True,  # Allow cookies & authentication
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# # Start video processing
# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(analyze_frame())


# Include routers
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(stream.router, prefix="/api/v1", tags=["insights"])
app.include_router(health.router, tags=["health"])

app.get("/")
async def root():
    return {"message": "Welcome to the Agora Vision Insights API!"}