from pydantic import BaseModel
from typing import List, Optional, Union, Any


# Unified request model for all media types
class MediaRequest(BaseModel):
    mood: str
    media_type: str  # "music", "movies", "books", "podcasts"
    limit: Optional[int] = 10


# Individual media item models
class Track(BaseModel):
    name: str
    artist: str
    album: str
    spotify_url: str
    preview_url: Optional[str]
    image_url: Optional[str]
    popularity: Optional[int]
    duration_ms: Optional[int]
    media_type: str = "music"


class Movie(BaseModel):
    title: str
    director: Optional[str]
    year: Optional[int]
    genres: List[str]
    tmdb_url: str
    poster_url: Optional[str]
    rating: Optional[float]
    synopsis: Optional[str]
    runtime: Optional[int]
    media_type: str = "movie"


class Book(BaseModel):
    title: str
    author: str
    isbn: Optional[str]
    year: Optional[int]
    genres: List[str]
    google_books_url: str
    cover_url: Optional[str]
    rating: Optional[float]
    description: Optional[str]
    page_count: Optional[int]
    media_type: str = "book"


class Podcast(BaseModel):
    title: str
    creator: str
    categories: List[str]
    spotify_url: str
    cover_url: Optional[str]
    description: Optional[str]
    total_episodes: Optional[int]
    media_type: str = "podcast"


# Unified response model
class MediaRecommendationResponse(BaseModel):
    mood: str
    media_type: str
    results: List[Any]  # Will contain Track, Movie, Book, or Podcast objects
    total_found: int


# Legacy models for backward compatibility
class MoodRequest(BaseModel):
    mood: str
    limit: Optional[int] = 10


class RecommendationResponse(BaseModel):
    mood: str
    tracks: List[Track]
    total_found: int