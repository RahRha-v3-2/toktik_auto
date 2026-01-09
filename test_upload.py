#!/usr/bin/env python3
"""
Test Video Upload - Process actual drone video for TikTok
"""

import os
import json
from video_processor import create_video_processor
from tiktok_manager import create_tiktok_manager

class TestVideoUpload:
    """Test upload with real video file"""
    
    def __init__(self):
        self.load_content()
        self.setup_components()
    
    def load_content(self):
        """Load generated content"""
        with open('production_config.json', 'r') as f:
            config = json.load(f)
        self.posts = config['posting_schedule']
    
    def setup_components(self):
        """Setup processing components"""
        # Use mock video processor (FFmpeg not available)
        self.video_processor = create_video_processor(use_mock=True)
        # Use real TikTok manager
        self.tiktok_manager = create_tiktok_manager(use_mock=False)
    
    def process_actual_video(self):
        """Process the content_1.mp4 video"""
        print("🎬 PROCESSING ACTUAL DRONE VIDEO")
        print("=" * 50)
        
        # Find the video
        video_path = "videos/content_1.mp4"
        if not os.path.exists(video_path):
            print(f"❌ Video not found: {video_path}")
            return False
        
        print(f"✅ Found video: {video_path}")
        
        # Get video info
        info = self.video_processor.get_video_info(video_path)
        print(f"📊 Video Info:")
        print(f"   Duration: {info.get('duration', 'Unknown')} seconds")
        print(f"   Resolution: {info.get('width', '?')}x{info.get('height', '?')}")
        print(f"   FPS: {info.get('fps', '?')}")
        
        # Get matching content
        post_1 = self.posts[0]  # First post matches content_1
        content = post_1['content']
        
        print(f"\n📋 MATCHING CONTENT:")
        print(f"   Idea: {content['idea']}")
        print(f"   Caption: {content['tiktok_caption']}")
        print(f"   Score: {content['content_score']}/100")
        print(f"   Hashtags: {', '.join(content['optimal_hashtags'])}")
        
        return True
    
    def simulate_video_processing(self):
        """Simulate video processing pipeline"""
        print(f"\n🎥 VIDEO PROCESSING PIPELINE")
        print("-" * 40)
        
        video_path = "videos/content_1.mp4"
        
        # Step 1: Check format
        print("1️⃣ Checking video format...")
        info = self.video_processor.get_video_info(video_path)
        width = info.get('width', 0)
        height = info.get('height', 0)
        
        if height > width:  # Vertical video
            print("   ✅ Already vertical format (good for TikTok)")
        else:
            print("   🔄 Needs resizing to 1080x1920")
        
        # Step 2: Resize (mock)
        print("2️⃣ Resizing to TikTok format...")
        result = self.video_processor.resize_video(
            video_path, 
            "videos/content_1_resized.mp4"
        )
        if result:
            print("   ✅ Resizing completed")
        else:
            print("   ⚠️  Resizing simulated (mock mode)")
        
        # Step 3: Enhance colors
        print("3️⃣ Applying cinematic enhancements...")
        result = self.video_processor.enhance_video(
            "videos/content_1_resized.mp4",
            "videos/content_1_enhanced.mp4"
        )
        if result:
            print("   ✅ Enhancement completed")
        else:
            print("   ⚠️  Enhancement simulated (mock mode)")
        
        # Step 4: Add text overlay
        print("4️⃣ Adding text overlay...")
        post_1 = self.posts[0]
        caption = post_1['content']['tiktok_caption'][:30]
        result = self.video_processor.add_text_overlay(
            "videos/content_1_enhanced.mp4",
            "videos/content_1_final.mp4",
            caption
        )
        if result:
            print("   ✅ Text overlay added")
        else:
            print("   ⚠️  Text overlay simulated (mock mode)")
        
        return "videos/content_1_final.mp4"
    
    def test_tiktok_upload(self, final_video_path):
        """Test upload to TikTok"""
        print(f"\n📱 TESTING TIKTOK UPLOAD")
        print("-" * 40)
        
        # Get content for upload
        post_1 = self.posts[0]
        content = post_1['content']
        
        print("🔑 Getting TikTok access token...")
        token = self.tiktok_manager.get_access_token()
        if token:
            print(f"   ✅ Token obtained: {token[:20]}...")
        else:
            print("   ❌ Failed to get token")
            return False
        
        print("📤 Attempting video upload...")
        result = self.tiktok_manager.upload_video(
            final_video_path,
            content['tiktok_caption'],
            content['optimal_hashtags']
        )
        
        if result.get("success"):
            print(f"   ✅ Upload successful!")
            print(f"   📹 Video ID: {result.get('video_id')}")
            print(f"   📊 Status: {result.get('status')}")
        else:
            print(f"   ⚠️  Upload issue: {result.get('error')}")
            print("   📝 This is expected - requires user OAuth setup")
        
        return result.get("success", False)
    
    def show_final_status(self, upload_success):
        """Show final processing status"""
        print(f"\n📊 FINAL STATUS")
        print("=" * 50)
        
        print(f"🎬 Video File: videos/content_1.mp4")
        print(f"📊 File Size: {os.path.getsize('videos/content_1.mp4')/1024/1024:.1f} MB")
        
        if upload_success:
            print("✅ Upload Status: SUCCESS")
            print("🚀 Ready for TikTok posting!")
        else:
            print("⚠️  Upload Status: NEEDS SETUP")
            print("🔧 Required: User OAuth flow in TikTok Developer Console")
        
        print(f"\n📋 Content Details:")
        post_1 = self.posts[0]
        content = post_1['content']
        print(f"   🎯 Score: {content['content_score']}/100")
        print(f"   ⏰ Scheduled: {post_1['scheduled_time']}")
        print(f"   📝 Caption: {content['tiktok_caption']}")
        print(f"   #️⃣ Hashtags: {', '.join(content['optimal_hashtags'])}")
    
    def run_test(self):
        """Run complete video upload test"""
        print("🚀 TESTING VIDEO UPLOAD PIPELINE")
        print("=" * 60)
        
        # Process actual video
        if self.process_actual_video():
            # Simulate processing
            final_video = self.simulate_video_processing()
            
            # Test upload
            upload_success = self.test_tiktok_upload(final_video)
            
            # Show final status
            self.show_final_status(upload_success)
        else:
            print("❌ No video found to process")

def main():
    """Run video upload test"""
    tester = TestVideoUpload()
    tester.run_test()
    
    print(f"\n🎉 VIDEO UPLOAD TEST COMPLETE!")
    print(f"📋 Next Steps:")
    print(f"   1. Add content_2.mp4 and content_3.mp4")
    print(f"   2. Complete TikTok user OAuth setup")  
    print(f"   3. Run automated posting: python3 main.py --real --scheduler")
    print(f"   4. Monitor your TikTok channel growth!")

if __name__ == "__main__":
    main()