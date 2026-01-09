#!/usr/bin/env python3
"""
Video Content Viewer - Match Real Drone Footage to Generated Content
Shows you exactly how to pair your drone videos with generated scripts
"""

import os
import json
from datetime import datetime

class VideoContentViewer:
    """View and match generated content with actual drone videos"""
    
    def __init__(self):
        self.load_generated_content()
        self.create_video_library_template()
    
    def load_generated_content(self):
        """Load the generated content from production config"""
        try:
            with open('production_config.json', 'r') as f:
                self.config = json.load(f)
                self.scheduled_posts = self.config['posting_schedule']
            print("✅ Generated content loaded successfully")
        except Exception as e:
            print(f"❌ Error loading content: {e}")
            self.scheduled_posts = []
    
    def create_video_library_template(self):
        """Create template for organizing your drone videos"""
        video_structure = {
            "video_library": {
                "wildlife": {
                    "description": "Wildlife herd tracking from aerial distance",
                    "required_shots": [
                        "Wide shot of herd from above",
                        "Smooth circular movement", 
                        "Horizontal tracking following movement",
                        "Pull back to wide environmental shot"
                    ],
                    "video_files": []
                },
                "city_skyline": {
                    "description": "City skyline during blue hour",
                    "required_shots": [
                        "Wide establishing shot of skyline",
                        "Low-angle horizontal tracking",
                        "Golden hour light capture", 
                        "Fade out with city lights"
                    ],
                    "video_files": []
                },
                "urban_tour": {
                    "description": "Urban city drone tour with music sync",
                    "required_shots": [
                        "Vertical ascent from street level",
                        "Forward glide through buildings",
                        "Tracking shot of moving traffic",
                        "Dramatic pause on landmark"
                    ],
                    "video_files": []
                },
                "sunset_drone": {
                    "description": "Epic sunset drone reveal",
                    "required_shots": [
                        "Start close on landscape feature",
                        "Smooth upward reveal", 
                        "Wide shot of full sunset",
                        "Cinematic fade to black"
                    ],
                    "video_files": []
                }
            }
        }
        
        if not os.path.exists('video_library.json'):
            with open('video_library.json', 'w') as f:
                json.dump(video_structure, f, indent=2)
            print("📁 Created video library template: video_library.json")
        
        return video_structure
    
    def display_content_matches(self):
        """Show how to match content with videos"""
        print("\n🎬 VIDEO CONTENT MATCHING GUIDE")
        print("=" * 60)
        
        for i, post in enumerate(self.scheduled_posts, 1):
            content = post['content']
            idea = content['idea']
            script = content['script']
            
            print(f"\n📹 POST {i}: {idea}")
            print(f"⏰ Scheduled: {post['scheduled_time'][:10]} at {post['scheduled_time'][11:16]}")
            print(f"📊 Score: {content['content_score']}/100")
            
            print(f"\n📋 REQUIRED VIDEO SCENES:")
            movements = script['movements']
            for j, movement in enumerate(movements, 1):
                print(f"   {j}. {movement}")
            
            print(f"\n🎬 SHOOTING INSTRUCTIONS:")
            print(f"   📍 Location: {self._get_location_suggestion(idea)}")
            print(f"   ⏰ Time: {self._get_time_suggestion(script)}")
            print(f"   🎵 Music: {script['music']}")
            print(f"   🎨 Style: {script['story']}")
            
            print(f"\n📝 FINAL CAPTION:")
            print(f"   {content['tiktok_caption']}")
            print(f"   #️⃣ {', '.join(content['optimal_hashtags'][:3])}")
            
            print("─" * 50)
    
    def _get_location_suggestion(self, idea):
        """Get location suggestion based on content idea"""
        if "wildlife" in idea.lower():
            return "Nature reserve, safari park, or open wilderness"
        elif "city" in idea.lower() or "urban" in idea.lower():
            return "Downtown area, rooftop, or elevated viewpoint"
        elif "harbor" in idea.lower() or "marina" in idea.lower():
            return "Coastal harbor, marina, or waterfront"
        elif "mountain" in idea.lower():
            return "Mountain peak, ridge line, or elevated vista"
        elif "beach" in idea.lower() or "ocean" in idea.lower():
            return "Beach coastline, cliff edge, or sand dunes"
        else:
            return "Scenic location with interesting features"
    
    def _get_time_suggestion(self, script):
        """Get time suggestion based on music and style"""
        music = script.get('music', '').lower()
        if 'sunset' in music or 'golden' in music:
            return "Golden hour (5:30-7:30 PM)"
        elif 'blue' in music:
            return "Blue hour (6:30-8:00 AM or 7:30-9:00 PM)"
        elif 'night' in music:
            return "Nighttime with city lights"
        elif 'sunrise' in music or 'morning' in music:
            return "Early morning (5:30-7:30 AM)"
        else:
            return "Daylight with good visibility"
    
    def create_shooting_checklist(self):
        """Create shooting checklist for each content type"""
        print("\n📋 SHOOTING CHECKLISTS")
        print("=" * 60)
        
        checklists = {
            "Wildlife Tracking": [
                "✅ Drone battery fully charged",
                "✅ Wildlife location scouted", 
                "✅ Weather conditions clear",
                "✅ Animals present and active",
                "✅ Wide establishing shot (10 seconds)",
                "✅ Circular tracking shot (15 seconds)",
                "✅ Horizontal following shot (10 seconds)",
                "✅ Pull back to environment (5 seconds)",
                "✅ Total 30-40 seconds footage"
            ],
            "City Skyline": [
                "✅ Battery charged for altitude",
                "✅ Legal airspace checked",
                "✅ Blue hour timing planned",
                "✅ Wide city establishing shot",
                "✅ Low-angle tracking pass",
                "✅ Golden hour light capture",
                "✅ Smooth camera movements",
                "✅ City lights visible"
            ],
            "Urban Tour": [
                "✅ Obstacle avoidance ready",
                "✅ Route planned through buildings",
                "✅ Synchronization music ready",
                "✅ Vertical ascent from ground",
                "✅ Forward glide sequences",
                "✅ Traffic or people tracking",
                "✅ Landmark focus shots",
                "✅ Dynamic movements"
            ]
        }
        
        for title, checklist in checklists.items():
            print(f"\n🎬 {title}:")
            for item in checklist:
                print(f"   {item}")
    
    def display_video_upload_workflow(self):
        """Show how to upload and process videos"""
        print("\n📤 VIDEO UPLOAD WORKFLOW")
        print("=" * 60)
        
        print("\n🔥 STEP 1: Organize Footage")
        print("   📁 Create folder: drone_footage/")
        print("   📁 Subfolders: wildlife/, city/, urban/, sunset/")
        print("   🎬 Name files: wildlife_001.mp4, wildlife_002.mp4")
        
        print("\n🎥 STEP 2: Basic Editing")
        print("   ✂️ Trim to 30-40 seconds")
        print("   🎨 Color grade for cinematic look")
        print("   🎵 Add background music")
        print("   📱 Export in 1080x1920 (TikTok format)")
        
        print("\n⚙️ STEP 3: Upload to System")
        print("   💾 Place videos in /videos/ folder")
        print("   🏷️ Match filenames to content IDs")
        print("   🔄 Run: python3 main.py --process-videos")
        
        print("\n🚀 STEP 4: Auto-Posting")
        print("   🤖 System matches videos to scripts")
        print("   📱 Uploads to TikTok automatically")
        print("   ⏰ Posts at optimal times")
        print("   📊 Tracks performance")
    
    def create_video_template(self):
        """Create template filename structure"""
        print("\n📂 VIDEO FILE NAMING TEMPLATE")
        print("=" * 60)
        
        template = """
🎯 VIDEO NAMING CONVENTION:
   
Format: {content_type}_{quality}_{location}_{date}_{version}.mp4

Examples:
├── wildlife_4K_serengeti_2025-01-08_v001.mp4
├── city_1080_nyc_2025-01-10_v001.mp4  
├── urban_4K_london_2025-01-12_v001.mp4
└── sunset_1080_california_2025-01-14_v001.mp4

📋 MATCHING TO GENERATED CONTENT:
├── post_1 → wildlife_tracking_4K.mp4
├── post_2 → city_skyline_1080.mp4
└── post_3 → urban_tour_4K.mp4
        """
        
        print(template)
    
    def run_full_viewer(self):
        """Run complete content viewer"""
        print("🎬 DRONE VIDEO CONTENT VIEWER")
        print("=" * 60)
        
        self.display_content_matches()
        self.create_shooting_checklist() 
        self.display_video_upload_workflow()
        self.create_video_template()
        
        print(f"\n✅ CONTENT VIEWER COMPLETE!")
        print(f"📁 Check 'video_library.json' for video organization")
        print(f"🎬 Use the checklists to shoot perfect footage")
        print(f"📱 Follow the upload workflow to integrate videos")

def main():
    """Run the video content viewer"""
    viewer = VideoContentViewer()
    viewer.run_full_viewer()
    
    print(f"\n🚀 NEXT STEPS:")
    print(f"1. Shoot drone footage using the checklists")
    print(f"2. Organize videos in the recommended structure") 
    print(f"3. Run: python3 main.py --real --process-videos")
    print(f"4. Watch your TikTok channel grow! 🎉")

if __name__ == "__main__":
    main()