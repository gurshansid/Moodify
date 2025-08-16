from fastapi import APIRouter, HTTPException
from app.models import MoodRequest, RecommendationResponse
from app.services.openai_service import OpenAIService
from app.services.spotify_service import SpotifyService

router = APIRouter()


@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: MoodRequest):
    """
    Get music recommendations based on mood
    """
    try:
        # Get AI recommendations
        openai_service = OpenAIService()
        song_queries = await openai_service.get_music_recommendations(
            mood=request.mood,
            limit=request.limit
        )
        
        if not song_queries:
            raise HTTPException(status_code=404, detail="No recommendations found")
        
        # Search Spotify for tracks
        spotify_service = SpotifyService()
        tracks = await spotify_service.search_tracks(song_queries)
        
        return RecommendationResponse(
            mood=request.mood,
            tracks=tracks,
            total_found=len(tracks)
        )
        
    except Exception as e:
        print(f"Error in get_recommendations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "music-recommendation-api"}