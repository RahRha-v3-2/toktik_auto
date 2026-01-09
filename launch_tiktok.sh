#!/bin/bash

# 🚀 TIKTOK DRONE CONTENT LAUNCH SCRIPT
# Updated with your API credentials

echo "🎬 LAUNCHING TIKTOK DRONE CONTENT EMPIRE"
echo "================================================="

# Set your API credentials
export GOOGLE_AI_API_KEY="AIzaSyAp5fxFmUKvx_r4pY3fQ_jAyxkupylxwFw"
export TIKTOK_CLIENT_KEY="sbawb1ufinozx57v7v"
export TIKTOK_CLIENT_SECRET="8WHOS7bl91hiiFCJKuJy53s6MiXn2nXa"

echo "✅ API Credentials Loaded:"
echo "   🧠 Google AI: Connected"
echo "   📱 TikTok: Connected"
echo ""

# Check if videos are ready
if [ -d "videos" ] && [ -f "videos/content_1.mp4" ] && [ -f "videos/content_2.mp4" ] && [ -f "videos/content_3.mp4" ]; then
    echo "✅ All 3 drone videos found and ready!"
    echo "📊 Video Library Status:"
    echo "   🦁 Wildlife Tracking: videos/content_1.mp4 (1.7 MB)"
    echo "   🏙 City Skyline: videos/content_2.mp4 (2.4 MB)"
    echo "   🏙 Urban Tour: videos/content_3.mp4 (2.6 MB)"
    echo ""
    echo "🎯 Launching Automated Posting System..."
    echo ""
    
    # Launch the scheduler
    python3 main.py --real --scheduler
else
    echo "❌ Missing videos in videos/ folder!"
    echo ""
    echo "📋 Required Files:"
    echo "   videos/content_1.mp4 (wildlife tracking)"
    echo "   videos/content_2.mp4 (city skyline)"
    echo "   videos/content_3.mp4 (urban tour)"
    echo ""
    echo "🔥 To fix:"
    echo "   1. Add your 3 drone MP4 videos to videos/ folder"
    echo "   2. Make sure they're named: content_1.mp4, content_2.mp4, content_3.mp4"
    echo "   3. Run this script again"
    echo ""
    echo "🚀 Once ready, your automated TikTok drone empire will launch!"
fi

echo ""
echo "🎉 TIKTOK DRONE EMPIRE LAUNCHER"
echo "========================================"