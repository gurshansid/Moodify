import os
import requests
from typing import List, Optional
from app.models import Movie


class TMDbService:
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"

    async def search_movies(self, movie_queries: List[str]) -> List[Movie]:
        """
        Search for movies on TMDb based on movie queries
        """
        movies = []
        
        for query in movie_queries:
            try:
                # Search for the movie
                search_url = f"{self.base_url}/search/movie"
                params = {
                    'api_key': self.api_key,
                    'query': query.split(' - ')[0] if ' - ' in query else query,  # Extract movie title
                    'language': 'en-US',
                    'page': 1,
                    'include_adult': False
                }
                
                response = requests.get(search_url, params=params)
                response.raise_for_status()
                
                search_results = response.json()
                
                if search_results['results']:
                    movie_data = search_results['results'][0]  # Take first result
                    
                    # Get additional details
                    movie_details = await self._get_movie_details(movie_data['id'])
                    
                    # Get director from credits
                    director = await self._get_movie_director(movie_data['id'])
                    
                    # Build poster URL
                    poster_url = None
                    if movie_data.get('poster_path'):
                        poster_url = f"{self.image_base_url}{movie_data['poster_path']}"
                    
                    movie = Movie(
                        title=movie_data['title'],
                        director=director,
                        year=int(movie_data['release_date'][:4]) if movie_data.get('release_date') else None,
                        genres=[genre['name'] for genre in movie_details.get('genres', [])],
                        tmdb_url=f"https://www.themoviedb.org/movie/{movie_data['id']}",
                        poster_url=poster_url,
                        rating=round(movie_data.get('vote_average', 0), 1) if movie_data.get('vote_average') else None,
                        synopsis=movie_data.get('overview'),
                        runtime=movie_details.get('runtime')
                    )
                    
                    movies.append(movie)
                    
            except Exception as e:
                print(f"Error searching for movie '{query}': {e}")
                continue
        
        return movies

    async def _get_movie_details(self, movie_id: int) -> dict:
        """Get detailed movie information"""
        try:
            details_url = f"{self.base_url}/movie/{movie_id}"
            params = {
                'api_key': self.api_key,
                'language': 'en-US'
            }
            
            response = requests.get(details_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting movie details: {e}")
            return {}

    async def _get_movie_director(self, movie_id: int) -> Optional[str]:
        """Get movie director from credits"""
        try:
            credits_url = f"{self.base_url}/movie/{movie_id}/credits"
            params = {
                'api_key': self.api_key
            }
            
            response = requests.get(credits_url, params=params)
            response.raise_for_status()
            credits = response.json()
            
            # Find director in crew
            for crew_member in credits.get('crew', []):
                if crew_member.get('job') == 'Director':
                    return crew_member.get('name')
            
            return None
        except Exception as e:
            print(f"Error getting movie director: {e}")
            return None