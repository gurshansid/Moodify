import os
from openai import OpenAI
from typing import List
import json
import re
import random


class MediaAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_fallback_recommendations(self, mood: str, media_type: str, limit: int = 10) -> List[str]:
        """
        Smart fallback recommendations based on mood keywords and media type
        """
        mood_lower = mood.lower()
        
        fallback_data = {
            "music": {
                "happy": ["Pharrell Williams - Happy", "The Beatles - Here Comes the Sun", "Queen - Don't Stop Me Now"],
                "sad": ["Johnny Cash - Hurt", "Mad World - Gary Jules", "Tears in Heaven - Eric Clapton"],
                "energetic": ["The Killers - Mr. Brightside", "Queen - We Will Rock You", "AC/DC - Thunderstruck"],
                "chill": ["Norah Jones - Come Away With Me", "Jack Johnson - Better Together", "Zero 7 - In the Waiting Line"],
                "romantic": ["Ed Sheeran - Perfect", "John Legend - All of Me", "Etta James - At Last"]
            },
            "movies": {
                "happy": ["The Grand Budapest Hotel", "Paddington", "The Princess Bride", "About Time"],
                "sad": ["Her", "Manchester by the Sea", "The Pursuit of Happyness", "Inside Out"],
                "action": ["Mad Max: Fury Road", "John Wick", "The Dark Knight", "Mission: Impossible - Fallout"],
                "thriller": ["Gone Girl", "Zodiac", "No Country for Old Men", "Prisoners"],
                "comedy": ["Superbad", "Bridesmaids", "Knives Out", "Game Night"],
                "romantic": ["Before Sunrise", "The Notebook", "Her", "Casablanca"],
                "scary": ["Hereditary", "The Conjuring", "Get Out", "A Quiet Place"]
            },
            "books": {
                "happy": ["The Alchemist", "Eat Pray Love", "The Happiness Project", "Big Magic"],
                "sad": ["A Man Called Ove", "The Fault in Our Stars", "Me Before You", "The Light We Lost"],
                "thriller": ["Gone Girl", "The Girl with the Dragon Tattoo", "The Silent Patient", "Big Little Lies"],
                "romance": ["Pride and Prejudice", "The Notebook", "Me Before You", "It Ends with Us"],
                "inspiring": ["Atomic Habits", "The 7 Habits of Highly Effective People", "Educated", "Becoming"]
            },
            "podcasts": {
                "educational": ["Radiolab", "Stuff You Should Know", "TED Talks Daily", "The Daily"],
                "comedy": ["Conan O'Brien Needs a Friend", "My Dad Wrote A Porno", "Comedy Bang! Bang!", "The Joe Rogan Experience"],
                "true_crime": ["Serial", "My Favorite Murder", "Criminal", "Dateline NBC"],
                "business": ["How I Built This", "The Tim Ferriss Show", "Masters of Scale", "Planet Money"],
                "storytelling": ["This American Life", "The Moth", "Reply All", "Heavyweight"]
            }
        }
        
        # Default recommendations
        default_items = fallback_data.get(media_type, {}).get("happy", [
            "The Shawshank Redemption" if media_type == "movies" else 
            "The Beatles - Here Comes the Sun" if media_type == "music" else
            "The Alchemist" if media_type == "books" else
            "This American Life"
        ])
        
        # Find matching category
        media_data = fallback_data.get(media_type, {})
        selected_items = default_items
        
        for category, items in media_data.items():
            if category in mood_lower:
                selected_items = items
                break
        
        # Additional keyword matching
        if media_type == "movies":
            if any(word in mood_lower for word in ["laugh", "funny", "humor"]):
                selected_items = media_data.get("comedy", default_items)
            elif any(word in mood_lower for word in ["fear", "horror", "scary"]):
                selected_items = media_data.get("scary", default_items)
            elif any(word in mood_lower for word in ["action", "adrenaline", "explosive"]):
                selected_items = media_data.get("action", default_items)
        elif media_type == "podcasts":
            if any(word in mood_lower for word in ["learn", "educational", "knowledge"]):
                selected_items = media_data.get("educational", default_items)
            elif any(word in mood_lower for word in ["business", "entrepreneur", "startup"]):
                selected_items = media_data.get("business", default_items)
            elif any(word in mood_lower for word in ["crime", "mystery", "murder"]):
                selected_items = media_data.get("true_crime", default_items)
        
        random.shuffle(selected_items)
        return selected_items[:limit]

    async def get_media_recommendations(self, mood: str, media_type: str, limit: int = 10) -> List[str]:
        """
        Get recommendations for any media type based on mood
        """
        # Customize prompt based on media type
        media_prompts = {
            "music": "songs that would match this mood. Return in format ['Artist - Song Title', ...]",
            "movies": "movies that would match this mood. Return just movie titles ['Movie Title', ...]",
            "books": "books that would match this mood. Return in format ['Book Title by Author', ...]",
            "podcasts": "podcasts that would match this mood. Return just podcast names ['Podcast Name', ...]"
        }
        
        prompt_template = media_prompts.get(media_type, media_prompts["music"])
        
        prompt = f"""
Based on the mood/feeling: "{mood}", recommend {limit} {prompt_template}

Please return ONLY a JSON array of strings in the exact format specified above.
Focus on popular, well-known {media_type} that would be found in major databases.
Make sure each entry follows the specified format exactly.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a {media_type} recommendation expert. Return only valid JSON arrays with no additional text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            content = response.choices[0].message.content.strip()
            
            # Extract JSON array from the response
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                recommendations = json.loads(json_str)
                return recommendations[:limit]
            else:
                # Fallback parsing
                lines = content.strip().split('\n')
                recommendations = []
                for line in lines:
                    line = line.strip().strip('"').strip("'").strip(',')
                    if line and len(recommendations) < limit:
                        recommendations.append(line)
                return recommendations

        except Exception as e:
            print(f"OpenAI API error for {media_type}: {e}")
            return self.get_fallback_recommendations(mood, media_type, limit)