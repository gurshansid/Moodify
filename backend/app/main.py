from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routes.recommendations import router as recommendations_router

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Music Recommendation API",
    description="Get music recommendations based on your mood",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommendations_router, prefix="/api", tags=["recommendations"])


@app.get("/")
async def root():
    return {"message": "Music Recommendation API is running!"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)