export interface Track {
    name: string;
    artist: string;
    album: string;
    spotify_url: string;
    preview_url?: string;
    image_url?: string;
    popularity?: number;
    duration_ms?: number;
  }
  
  export interface RecommendationResponse {
    mood: string;
    tracks: Track[];
    total_found: number;
  }
  
  export interface MoodRequest {
    mood: string;
    limit?: number;
  }