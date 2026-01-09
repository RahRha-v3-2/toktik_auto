#!/usr/bin/env python3
"""
Mock Content Generator for Testing
Simulates content generation when API is unavailable
"""

import json
import random
from datetime import datetime
from typing import List, Dict

class MockContentGenerator:
    """Mock content generator for testing without API"""
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.mock_ideas = [
            "Epic mountain sunrise drone reveal with cinematic transitions",
            "Urban city drone tour at golden hour with music sync",
            "Beach wave tracking drone shot from above",
            "Forest canopy fly-through with autumn colors",
            "Desert sand dunes drone photography at sunset",
            "Waterfall drone capture from multiple angles",
            "Harbor and marina drone shots during sunrise",
            "Snow-covered mountain peak drone exploration",
            "Agricultural field patterns from bird's eye view",
            "Construction site time-lapse drone progression",
            "Island hopping coastal drone adventure",
            "Northern lights drone chase in arctic conditions",
            "City skyline drone shot during blue hour",
            "River following drone journey from source to mouth",
            "Wildlife herd tracking from safe aerial distance"
        ]
        
        self.mock_scripts = {
            "opening": ["Start with wide establishing shot", "Begin with close-up detail", "Open with dynamic movement"],
            "movements": ["Smooth glide forward", "Orbital circle around subject", "Vertical ascent reveal", "Horizontal tracking shot"],
            "story": ["Show scale and perspective", "Create sense of wonder", "Reveal hidden beauty", "Capture emotion of place"],
            "closing": ["Pull back to wide shot", "Fade to black with logo", "End with dramatic pause"],
            "music": ["Ambient electronic", "Cinematic orchestral", "Upbeat pop remix", "Nature sounds with gentle beat"],
            "hashtags": ["#drone", "#cinematic", "#photography", "#nature", "#travel"]
        }
    
    def generate_content_ideas(self, theme: str = "viral drone content", count: int = 5) -> List[str]:
        """Generate mock content ideas"""
        selected = random.sample(self.mock_ideas, min(count, len(self.mock_ideas)))
        
        # Add theme-specific variations
        if "viral" in theme.lower():
            selected = [f"VIRAL: {idea}" for idea in selected]
        
        return selected
    
    def generate_video_script(self, idea: str, duration: str = "30 seconds") -> Dict:
        """Generate mock video script"""
        script = {
            "opening": random.choice(self.mock_scripts["opening"]),
            "movements": [random.choice(self.mock_scripts["movements"]) for _ in range(3)],
            "story": random.choice(self.mock_scripts["story"]),
            "closing": random.choice(self.mock_scripts["closing"]),
            "music": random.choice(self.mock_scripts["music"]),
            "hashtags": random.sample(self.mock_scripts["hashtags"], 4)
        }
        
        return script
    
    def generate_caption(self, video_description: str, platform: str = "tiktok") -> str:
        """Generate mock caption"""
        captions = [
            f"🚁 Incredible drone shot! {video_description[:30]}... #drone #cinematic",
            f"✨ This view is just breathtaking! #dronephotography #nature",
            f"🎬 cinematic drone magic ✨ #dji #mavic #drone",
            f"From above everything looks different 🌍 #aerial #photography",
            f"Drone life is the best life! 🚁✨ #dronelife #adventure"
        ]
        
        caption = random.choice(captions)
        
        if platform == "tiktok":
            # Keep it short for TikTok
            if len(caption) > 150:
                caption = caption[:147] + "..."
        
        return caption
    
    def generate_drone_tips(self, skill_level: str = "beginner") -> List[str]:
        """Generate mock drone tips"""
        beginner_tips = [
            "Always check weather conditions before flying",
            "Start with basic maneuvers in an open area",
            "Learn to use gimbal controls for smooth footage",
            "Practice emergency landing procedures",
            "Keep your drone within line of sight initially"
        ]
        
        advanced_tips = [
            "Master complex flight paths for cinematic shots",
            "Use ND filters for better exposure control",
            "Learn manual camera settings for professional look",
            "Practice precision flying through tight spaces",
            "Understand airspace regulations and restrictions"
        ]
        
        tips = beginner_tips if skill_level == "beginner" else advanced_tips
        return random.sample(tips, 3)
    
    def analyze_trending_drone_content(self) -> Dict:
        """Generate mock trend analysis"""
        return {
            "analysis": """
📈 CURRENT DRONE CONTENT TRENDS:

🎥 Popular Shot Types:
- Top-down reveal shots
- Low-angle ascending shots  
- Tracking shots of moving subjects
- Golden hour cinematography

📍 Trending Locations:
- Desert landscapes at sunrise
- Urban cityscapes at blue hour
- Coastal wave formations
- Mountain peak reveals

🎬 Editing Styles:
- Smooth color grading
- Slow motion emphasis
- Cinematic sound design
- Quick cut transitions

🎵 Viral Music:
- Lo-fi hip hop beats
- Cinematic orchestral scores
- Trending remixes of popular songs
- Nature ambient sounds

⏰ Best Posting Times:
- Early morning: 6-8 AM
- Evening: 7-9 PM  
- Weekends have higher engagement
            """,
            "hashtags": ["#drone", "#cinematic", "#viral", "#photography", "#trending"]
        }
    
    def save_content(self, content: Dict, filename: str = None) -> str:
        """Save generated content to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"drone_content_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(content, f, indent=2)
        
        return filename