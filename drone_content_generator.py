#!/usr/bin/env python3
"""
Drone Content Generator Tool
Uses Google AI Studio to create drone-related content
"""

import os
import sys
import google.genai as genai
from typing import List, Dict, Optional
import json
from datetime import datetime

class DroneContentGenerator:
    def __init__(self, api_key: str):
        """Initialize the content generator with API key"""
        self.client = genai.Client(api_key=api_key)
        
    def generate_content_ideas(self, theme: str = "viral drone content", count: int = 5) -> List[str]:
        """Generate content ideas for drone videos"""
        prompt = f"""
        Generate {count} viral drone video content ideas. Focus on:
        - Trending drone cinematography techniques
        - Popular drone locations
        - Engaging storytelling with aerial footage
        - Social media friendly concepts
        
        Theme: {theme}
        
        Return as a numbered list with brief descriptions.
        """
        
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        return self._parse_list_response(response.candidates[0].content.parts[0].text)
    
    def generate_video_script(self, idea: str, duration: str = "30 seconds") -> Dict:
        """Generate a video script for drone footage"""
        prompt = f"""
        Create a drone video script for this idea: "{idea}"
        
        Duration: {duration}
        
        Include:
        1. Opening shot description
        2. Key drone movements and angles
        3. Story progression
        4. Closing shot
        5. Suggested background music type
        6. Hashtags for social media
        
        Format as JSON with keys: opening, movements, story, closing, music, hashtags
        """
        
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        try:
            return json.loads(response.candidates[0].content.parts[0].text)
        except:
            return {"raw_script": response.candidates[0].content.parts[0].text}
    
    def generate_caption(self, video_description: str, platform: str = "tiktok") -> str:
        """Generate social media captions for drone content"""
        prompt = f"""
        Create an engaging {platform} caption for this drone video:
        
        {video_description}
        
        Include:
        - Hook to grab attention
        - Relevant emojis
        - Call to action
        - Popular hashtags for drone content
        
        Keep it under 200 characters for TikTok, under 300 for Instagram.
        """
        
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        return response.candidates[0].content.parts[0].text.strip()
    
    def generate_drone_tips(self, skill_level: str = "beginner") -> List[str]:
        """Generate drone flying tips"""
        prompt = f"""
        Generate 5 practical drone flying tips for {skill_level} pilots.
        Focus on safety, technique, and getting better shots.
        """
        
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        return self._parse_list_response(response.candidates[0].content.parts[0].text)
    
    def analyze_trending_drone_content(self) -> Dict:
        """Analyze trending drone content patterns"""
        prompt = """
        Analyze current trends in drone content on social media. Include:
        1. Popular types of drone shots
        2. Trending locations
        3. Common editing styles
        4. Viral music choices
        5. Best posting times
        
        Return as JSON with trend analysis.
        """
        
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        try:
            return json.loads(response.candidates[0].content.parts[0].text)
        except:
            return {"analysis": response.candidates[0].content.parts[0].text}
    
    def _parse_list_response(self, response_text: str) -> List[str]:
        """Parse numbered list responses"""
        lines = response_text.strip().split('\n')
        items = []
        
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering and clean up
                clean_line = line
                if '.' in line[:5]:
                    clean_line = line.split('.', 1)[1].strip()
                elif ')' in line[:5]:
                    clean_line = line.split(')', 1)[1].strip()
                elif line.startswith('-'):
                    clean_line = line[1:].strip()
                
                if clean_line:
                    items.append(clean_line)
        
        return items
    
    def save_content(self, content: Dict, filename: Optional[str] = None) -> str:
        """Save generated content to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"drone_content_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(content, f, indent=2)
        
        return filename

def main():
    """Main function to run the content generator"""
    api_key = "AIzaSyAp5fxFmUKvx_r4pY3fQ_jAyxkupylxwFw"
    
    print("🚁 Drone Content Generator")
    print("=" * 40)
    
    generator = DroneContentGenerator(api_key)
    
    # Demo mode - run a few examples automatically
    print("\n🎯 Running demo examples...")
    
    # 1. Generate content ideas
    print("\n📹 Generating content ideas...")
    ideas = generator.generate_content_ideas("viral drone content")
    print(f"Content Ideas for 'viral drone content':")
    for i, idea in enumerate(ideas[:3], 1):
        print(f"{i}. {idea}")
    
    # 2. Generate drone tips
    print(f"\n✈️ Generating drone tips for beginners...")
    tips = generator.generate_drone_tips("beginner")
    print("Drone Tips for beginners:")
    for i, tip in enumerate(tips[:3], 1):
        print(f"{i}. {tip}")
    
    # 3. Generate a sample caption
    print(f"\n📝 Generating sample caption...")
    caption = generator.generate_caption("Amazing sunset drone footage over mountains", "tiktok")
    print("TikTok Caption:")
    print(caption)
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    main()