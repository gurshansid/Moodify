from fastapi import APIRouter, HTTPException
from app.models import MediaRequest, MediaRecommendationResponse, MoodRequest, RecommendationResponse
from app.services.media_ai_service import MediaAIService
from app.services.spotify_service import SpotifyService
from app.services.tmdb_service import TMDbService
from typing import List, Any

router = APIRouter()


@router.post("/media-recommendations", response_model=MediaRecommendationResponse)
async def get_media_recommendations(request: MediaRequest):
    """
    Get recommendations for any media type based on mood
    """
    try:
        # Get AI recommendations
        media_ai_service = MediaAIService()
        queries = await media_ai_service.get_media_recommendations(
            mood=request.mood,
            media_type=request.media_type,
            limit=request.limit
        )
        
        if not queries:
            raise HTTPException(status_code=404, detail="No recommendations found")
        
        results = []
        
        # Route to appropriate service based on media type
        if request.media_type == "music":
            spotify_service = SpotifyService()
            results = await spotify_service.search_tracks(queries)
        
        elif request.media_type == "movies":
            tmdb_service = TMDbService()
            results = await tmdb_service.search_movies(queries)
        
        elif request.media_type == "books":
            # TODO: Implement Google Books service
            # google_books_service = GoogleBooksService()
            # results = await google_books_service.search_books(queries)
            raise HTTPException(status_code=501, detail="Books not implemented yet")
        
        elif request.media_type == "podcasts":
            # TODO: Implement podcast service
            # podcast_service = PodcastService()
            # results = await podcast_service.search_podcasts(queries)
            raise HTTPException(status_code=501, detail="Podcasts not implemented yet")
        
        else:
            raise HTTPException(status_code=400, detail="Invalid media type. Use: music, movies, books, podcasts")
        
        return MediaRecommendationResponse(
            mood=request.mood,
            media_type=request.media_type,
            results=results,
            total_found=len(results)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_media_recommendations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Legacy endpoint for backward compatibility
@router.post("/recommendations", response_model=RecommendationResponse)
async def get_music_recommendations(request: MoodRequest):
    """
    Legacy music recommendations endpoint (backward compatibility)
    """
    # Convert to MediaRequest
    media_request = MediaRequest(
        mood=request.mood,
        media_type="music",
        limit=request.limit
    )
    
    # Call the unified endpoint
    media_response = await get_media_recommendations(media_request)
    
    # Convert back to legacy format
    return RecommendationResponse(
        mood=media_response.mood,
        tracks=media_response.results,
        total_found=media_response.total_found
    )


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "unified-media-recommendation-api"}


@router.get("/supported-media-types")
async def get_supported_media_types():
    """
    Get list of supported media types
    """
    return {
        "supported_types": ["music", "movies"],
        "coming_soon": ["books", "podcasts"],
        "description": {
            "music": "Songs and tracks from Spotify",
            "movies": "Movies from The Movie Database (TMDb)",
            "books": "Books from Google Books API (coming soon)",
            "podcasts": "Podcasts from Spotify/Listen Notes (coming soon)"
        }
    }