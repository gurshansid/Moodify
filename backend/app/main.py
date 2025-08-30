from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routes.media import router as media_router

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Universal Media Recommendation API",
    description="Get music, movie, book, and podcast recommendations based on your mood",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include unified media router
app.include_router(media_router, prefix="/api", tags=["media"])


@app.get("/")
async def root():
    return {
        "message": "Universal Media Recommendation API is running!",
        "supported_media": ["music", "movies"],
        "coming_soon": ["books", "podcasts"],
        "version": "2.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)