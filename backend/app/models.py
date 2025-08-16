from pydantic import BaseModel
from typing import List, Optional


class MoodRequest(BaseModel):
    mood: str
    limit: Optional[int] = 10


class Track(BaseModel):
    name: str
    artist: str
    album: str
    spotify_url: str
    preview_url: Optional[str]
    image_url: Optional[str]
    popularity: Optional[int]
    duration_ms: Optional[int]


class RecommendationResponse(BaseModel):
    mood: str
    tracks: List[Track]
    total_found: int