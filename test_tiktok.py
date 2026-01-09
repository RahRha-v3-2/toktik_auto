#!/usr/bin/env python3
"""
TikTok API Test Script
Test TikTok API integration separately
"""

import os
from tiktok_manager import create_tiktok_manager

def test_tiktok_integration():
    """Test TikTok API integration"""
    print("🎬 Testing TikTok API Integration")
    print("=" * 40)
    
    # Use real TikTok credentials
    use_mock = False
    tiktok_manager = create_tiktok_manager(use_mock)
    
    print(f"Manager type: {type(tiktok_manager).__name__}")
    
    # Test access token
    print("\n🔑 Getting access token...")
    token = tiktok_manager.get_access_token()
    if token:
        print(f"✅ Access token obtained: {token[:20]}...")
    else:
        print("❌ Failed to get access token")
        return
    
    # Test trending hashtags
    print("\n#️⃣ Getting trending hashtags...")
    hashtags = tiktok_manager.search_trending_hashtags("drone")
    print(f"✅ Found {len(hashtags)} hashtags:")
    for i, tag in enumerate(hashtags[:5], 1):
        print(f"  {i}. {tag}")
    
    # Test mock upload (since we don't have real video)
    print("\n📤 Testing mock video upload...")
    result = tiktok_manager.upload_video(
        "test_video.mp4",
        "Amazing drone footage 🚁 #drone #cinematic",
        ["#drone", "#cinematic", "#aerial"]
    )
    
    if result.get("success"):
        print(f"✅ Upload successful! Video ID: {result.get('video_id')}")
    else:
        print(f"❌ Upload failed: {result.get('error')}")
    
    # Test getting user videos
    print("\n📋 Getting user videos...")
    videos = tiktok_manager.get_user_videos(5)
    print(f"✅ Found {len(videos)} videos:")
    for i, video in enumerate(videos[:3], 1):
        print(f"  {i}. {video.get('id', 'Unknown')} - {video.get('title', 'No title')[:30]}...")

if __name__ == "__main__":
    test_tiktok_integration()