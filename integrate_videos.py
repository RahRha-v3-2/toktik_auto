#!/usr/bin/env python3
"""
Video Integration Tool - Connect Real Drone Videos to Generated Content
"""

import os
import json
import shutil
from datetime import datetime

class VideoIntegrator:
    """Integrate real drone videos with generated content"""
    
    def __init__(self):
        self.load_content()
        self.scan_existing_videos()
    
    def load_content(self):
        """Load generated content"""
        with open('production_config.json', 'r') as f:
            self.config = json.load(f)
        self.posts = self.config['posting_schedule']
    
    def scan_existing_videos(self):
        """Scan for existing drone videos"""
        self.existing_videos = {}
        
        video_folders = ['drone_footage/wildlife', 'drone_footage/city', 
                      'drone_footage/urban', 'drone_footage/sunset', 'videos']
        
        for folder in video_folders:
            if os.path.exists(folder):
                videos = [f for f in os.listdir(folder) if f.endswith(('.mp4', '.mov', '.avi'))]
                self.existing_videos[folder] = videos
                print(f"📁 Found {len(videos)} videos in {folder}/")
        
        return self.existing_videos
    
    def create_sample_videos(self):
        """Create sample video files for demonstration"""
        sample_videos = {
            "videos/wildlife_tracking_demo.mp4": {
                "content_match": "post_1",
                "description": "Wildlife herd tracking from safe aerial distance",
                "required_scenes": ["Wide shot", "Circular tracking", "Horizontal follow", "Pull back"],
                "estimated_duration": "35 seconds"
            },
            "videos/city_skyline_demo.mp4": {
                "content_match": "post_2", 
                "description": "City skyline drone shot during blue hour",
                "required_scenes": ["Wide establishing", "Horizontal tracking", "Light capture", "Fade out"],
                "estimated_duration": "40 seconds"
            },
            "videos/urban_tour_demo.mp4": {
                "content_match": "post_3",
                "description": "Urban city drone tour at golden hour with music sync",
                "required_scenes": ["Vertical ascent", "Forward glide", "Traffic tracking", "Dramatic pause"],
                "estimated_duration": "30 seconds"
            }
        }
        
        print("\n🎬 Creating sample video references...")
        for video_path, info in sample_videos.items():
            # Create a text file to represent the video for demo
            demo_file = video_path.replace('.mp4', '_info.txt')
            with open(demo_file, 'w') as f:
                f.write(f"DEMO VIDEO REFERENCE\n")
                f.write(f"====================\n")
                f.write(f"File: {video_path}\n")
                f.write(f"Content Match: {info['content_match']}\n")
                f.write(f"Description: {info['description']}\n")
                f.write(f"Required Scenes:\n")
                for scene in info['required_scenes']:
                    f.write(f"  - {scene}\n")
                f.write(f"Duration: {info['estimated_duration']}\n")
                f.write(f"\nINSTRUCTIONS:\n")
                f.write(f"Replace this demo file with your actual drone footage!\n")
                f.write(f"Follow the scene requirements listed above.\n")
            
            print(f"✅ Created demo reference: {demo_file}")
        
        return sample_videos
    
    def match_videos_to_content(self):
        """Match available videos to generated content"""
        print("\n🎯 VIDEO-TO-CONTENT MATCHING")
        print("=" * 50)
        
        matches = []
        for i, post in enumerate(self.posts):
            content = post['content']
            post_id = post['post_id']
            
            print(f"\n📹 {post_id.upper()}: {content['idea']}")
            print(f"📊 Score: {content['content_score']}/100")
            
            # Find matching video
            matched_video = self._find_best_match(content, post_id)
            if matched_video:
                matches.append({
                    'post_id': post_id,
                    'video_path': matched_video,
                    'content': content
                })
                print(f"✅ MATCHED: {matched_video}")
            else:
                print(f"❌ NO MATCH - Add video to: videos/{post_id.replace('post_', 'content_')}.mp4")
            
            print(f"📝 Caption: {content['tiktok_caption']}")
            print(f"🎵 Music: {content['script']['music']}")
        
        return matches
    
    def _find_best_match(self, content, post_id):
        """Find best video match for content"""
        # Check for exact match first
        expected_name = f"{post_id.replace('post_', 'content_')}.mp4"
        
        # Check videos folder
        if os.path.exists('videos'):
            for file in os.listdir('videos'):
                if expected_name in file or any(keyword in file.lower() for keyword in ['wildlife', 'city', 'urban', 'sunset'] if keyword in content['idea'].lower()):
                    return f"videos/{file}"
        
        # Check other folders
        for folder, videos in self.existing_videos.items():
            for video in videos:
                if any(keyword in video.lower() for keyword in content['idea'].lower().split()):
                    return f"{folder}/{video}"
        
        return None
    
    def create_upload_script(self, matches):
        """Create script to upload matched videos"""
        print("\n📱 CREATING UPLOAD SCRIPT")
        print("=" * 50)
        
        upload_commands = []
        for match in matches:
            video_path = match['video_path']
            content = match['content']
            
            if os.path.exists(video_path):
                upload_commands.append(f"# Upload: {content['idea'][:30]}...")
                upload_commands.append(f"# Video: {video_path}")
                upload_commands.append(f"# Caption: {content['tiktok_caption']}")
                upload_commands.append(f"# Hashtags: {' '.join(content['optimal_hashtags'])}")
                upload_commands.append(f"# Score: {content['content_score']}/100")
                upload_commands.append("")
        
        script_content = "\n".join(upload_commands)
        
        with open('upload_script.sh', 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# TikTok Drone Video Upload Script\n")
            f.write("# Generated by TikTok Drone Content Generator\n\n")
            f.write("# Video Upload Commands\n")
            f.write(script_content)
        
        os.chmod('upload_script.sh', 0o755)
        print(f"✅ Created upload script: upload_script.sh")
    
    def display_current_status(self):
        """Display current video integration status"""
        print(f"\n📊 CURRENT INTEGRATION STATUS")
        print("=" * 50)
        
        total_posts = len(self.posts)
        matched_posts = len([m for m in self.match_videos_to_content() if m])
        
        print(f"📋 Total Posts Generated: {total_posts}")
        print(f"✅ Posts with Videos: {matched_posts}")
        print(f"❌ Posts Needing Videos: {total_posts - matched_posts}")
        print(f"📈 Ready to Post: {matched_posts}/{total_posts}")
        
        # Show video file locations
        print(f"\n📁 VIDEO FILE LOCATIONS:")
        print(f"   🎬 Main Folder: videos/")
        print(f"   🦁 Wildlife: drone_footage/wildlife/")
        print(f"   🏙 City: drone_footage/city/")
        print(f"   🏙 Urban: drone_footage/urban/")
        print(f"   🌅 Sunset: drone_footage/sunset/")
        
        # Show next steps
        print(f"\n🚀 NEXT ACTIONS:")
        if matched_posts < total_posts:
            print(f"   1. Add {total_posts - matched_posts} drone videos to videos/ folder")
            print(f"   2. Name them: content_1.mp4, content_2.mp4, etc.")
        print(f"   3. Run: python3 main.py --real --upload-videos")
        print(f"   4. Schedule automated posting")
    
    def create_video_guide(self):
        """Create comprehensive video shooting guide"""
        guide = """
# 🚁 DRONE VIDEO SHOOTING GUIDE
## How to Create Perfect Videos for Generated Content

### 🎯 REQUIRED VIDEO SPECIFICATIONS
- **Duration**: 30-40 seconds (TikTok optimal)
- **Resolution**: 1080x1920 (9:16 vertical)
- **Format**: MP4 (H.264 codec)
- **Frame Rate**: 24-30 FPS
- **Bitrate**: 8-12 Mbps

### 📋 CURRENTLY NEEDED VIDEOS:

#### 1. WILDLIFE TRACKING (Post 1)
**Location**: Nature reserve, safari park, or wilderness
**Time**: Golden hour (5:30-7:30 PM)
**Weather**: Clear, good visibility
**Shots Required**:
  - Wide establishing shot (herd visible) - 10 seconds
  - Smooth circular movement - 15 seconds  
  - Horizontal tracking movement - 10 seconds
  - Pull back to environment - 5 seconds
**Music Style**: Ambient electronic
**Caption**: 🚁 Incredible drone shot! #drone #cinematic

#### 2. CITY SKYLINE (Post 2)  
**Location**: Downtown rooftop or elevated viewpoint
**Time**: Blue hour (6:30-8:00 AM or 7:30-9:00 PM)
**Weather**: Clear city view
**Shots Required**:
  - Wide skyline establishing - 10 seconds
  - Low-angle horizontal pass - 10 seconds
  - Light capture from buildings - 15 seconds  
  - Fade with city lights - 5 seconds
**Music Style**: Nature sounds with gentle beat
**Caption**: ✨ This view is just breathtaking! #dronephotography

#### 3. URBAN TOUR (Post 3)
**Location**: Urban area with interesting architecture
**Time**: Golden hour (5:30-7:30 PM)
**Weather**: Good lighting, minimal wind
**Shots Required**:
  - Vertical ascent from ground - 8 seconds
  - Forward glide through streets - 12 seconds
  - Dynamic movement tracking - 10 seconds
  - Dramatic pause on landmark - 5 seconds
**Music Style**: Upbeat sync with movement
**Caption**: 🎬 cinematic drone magic ✨ #dji #mavic

### 🎥 SHOOTING CHECKLIST:
- [ ] Drone battery fully charged
- [ ] Memory card formatted
- [ ] Weather conditions checked
- [ ] Location permission verified
- [ ] Flight path planned
- [ ] Legal airspace checked
- [ ] ND filters ready (if needed)
- [ ] Backup battery available

### ✂️ EDITING WORKFLOW:
1. **Import footage** into editing software
2. **Trim** to 30-40 seconds
3. **Color grade** for cinematic look
4. **Add background music** (royalty-free)
5. **Export** as MP4, 1080x1920
6. **Name** file: content_X.mp4 (where X = post number)
7. **Place** in videos/ folder

### 📱 INTEGRATION:
Once videos are ready:
1. Place MP4 files in: videos/
2. Name as: content_1.mp4, content_2.mp4, content_3.mp4
3. Run: python3 main.py --real --upload-videos
4. System automatically posts to TikTok

### 🔥 VIRAL TIPS:
- Start with hook (first 3 seconds crucial)
- Include smooth camera movements
- Add trending music
- Use relevant hashtags
- Post at optimal times (7-9 PM)
- Engage with comments quickly
        """
        
        with open('VIDEO_SHOOTING_GUIDE.md', 'w') as f:
            f.write(guide)
        
        print(f"✅ Created comprehensive shooting guide: VIDEO_SHOOTING_GUIDE.md")
    
    def run_integration(self):
        """Run complete video integration"""
        print("🎬 DRONE VIDEO INTEGRATION SYSTEM")
        print("=" * 60)
        
        # Scan existing videos
        self.scan_existing_videos()
        
        # Create demo references
        self.create_sample_videos()
        
        # Match videos to content
        matches = self.match_videos_to_content()
        
        # Create upload script
        self.create_upload_script(matches)
        
        # Create shooting guide
        self.create_video_guide()
        
        # Display status
        self.display_current_status()
        
        print(f"\n🎉 INTEGRATION COMPLETE!")
        print(f"📁 Check these files:")
        print(f"   - videos/ folder (add your drone footage)")
        print(f"   - VIDEO_SHOOTING_GUIDE.md (shooting instructions)")
        print(f"   - upload_script.sh (upload automation)")

def main():
    """Run video integration"""
    integrator = VideoIntegrator()
    integrator.run_integration()

if __name__ == "__main__":
    main()