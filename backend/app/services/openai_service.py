import os
from openai import OpenAI
from typing import List
import json
import re


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def get_music_recommendations(self, mood: str, limit: int = 10) -> List[str]:
        """
        Get music recommendations based on mood using GPT-4
        """
        prompt = f"""
Based on the mood/feeling: "{mood}", recommend {limit} songs that would match this mood.

Please return ONLY a JSON array of strings in this exact format:
["Artist Name - Song Title", "Artist Name - Song Title", ...]

Focus on popular, well-known songs that are likely to be found on Spotify.
Make sure each entry follows the format "Artist Name - Song Title" exactly.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a music recommendation expert. Return only valid JSON arrays with no additional text."},
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
                    if ' - ' in line and len(recommendations) < limit:
                        recommendations.append(line)
                return recommendations

        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback recommendations
            return [
                "The Beatles - Here Comes the Sun",
                "Queen - Bohemian Rhapsody",
                "Led Zeppelin - Stairway to Heaven"
            ]