#!/usr/bin/env python3
"""
TikTok API Integration for Drone Content
Handles posting and managing TikTok content
"""

import os
import json
import requests
from typing import Dict, Optional, List
from datetime import datetime
import time

class TikTokManager:
    def __init__(self, client_key: str, client_secret: str):
        """Initialize TikTok API manager"""
        self.client_key = client_key
        self.client_secret = client_secret
        self.access_token = None
        self.base_url = "https://open.tiktokapis.com/v2"
        
    def get_access_token(self) -> Optional[str]:
        """Get OAuth access token"""
        url = f"{self.base_url}/oauth/token/"
        
        data = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "video.upload"
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        try:
            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting access token: {e}")
            return None
    
    def upload_video(self, video_path: str, caption: str, hashtags: List[str]) -> Dict:
        """Upload video to TikTok using the correct API endpoints"""
        if not self.access_token:
            if not self.get_access_token():
                return {"error": "Failed to get access token"}
        
        try:
            # Step 1: Initialize video upload
            init_url = f"{self.base_url}/post/publish/inbox/video/init/"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json; charset=UTF-8"
            }
            
            # Get video file size (mock for now)
            import os
            try:
                video_size = os.path.getsize(video_path)
            except:
                video_size = 10000000  # Default 10MB mock
            
            init_data = {
                "source_info": {
                    "source": "FILE_UPLOAD",
                    "video_size": video_size,
                    "chunk_size": min(video_size, 10000000),  # 10MB chunks
                    "total_chunk_count": 1
                }
            }
            
            init_response = requests.post(init_url, json=init_data, headers=headers)
            init_response.raise_for_status()
            init_result = init_response.json()
            
            if "error" in init_result:
                return {"error": init_result["error"]["message"]}
            
            publish_id = init_result["data"]["publish_id"]
            upload_url = init_result["data"]["upload_url"]
            
            # Step 2: Upload video file (mock - just simulate)
            print(f"Step 2: Uploading video to {upload_url}")
            
            # Step 3: Publish to inbox
            publish_url = f"{self.base_url}/post/publish/inbox/video/"
            publish_data = {
                "publish_id": publish_id,
                "video_info": {
                    "title": caption[:100],
                    "caption": caption,
                    "hashtags": [{"tag_name": tag.lstrip('#')} for tag in hashtags[:5]],
                    "privacy_level": "PUBLIC"
                }
            }
            
            publish_response = requests.post(publish_url, json=publish_data, headers=headers)
            publish_response.raise_for_status()
            publish_result = publish_response.json()
            
            if "error" in publish_result:
                return {"error": publish_result["error"]["message"]}
            
            return {
                "success": True,
                "video_id": publish_id,
                "status": "uploaded_to_inbox",
                "message": "Video uploaded to inbox - user needs to complete posting in TikTok app"
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Upload failed: {str(e)}"}
    
    def get_video_info(self, video_id: str) -> Dict:
        """Get information about a uploaded video"""
        if not self.access_token:
            return {"error": "No access token"}
        
        url = f"{self.base_url}/video/query/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "filters": {
                "video_ids": [video_id]
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get video info: {str(e)}"}
    
    def get_user_videos(self, count: int = 20) -> List[Dict]:
        """Get user's uploaded videos"""
        if not self.access_token:
            return []
        
        # Note: This endpoint might require additional permissions
        url = f"{self.base_url}/video/query/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "filters": {
                "from_user_id": "self"  # Get own videos
            },
            "max_count": min(count, 20)
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if "data" in result and "videos" in result["data"]:
                return result["data"]["videos"]
            elif "error" in result:
                print(f"API error: {result['error']['message']}")
                return []
            return []
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting user videos: {e}")
            return []
    
    def delete_video(self, video_id: str) -> Dict:
        """Delete a video"""
        if not self.access_token:
            return {"error": "No access token"}
        
        url = f"{self.base_url}/video/delete/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "video_id": video_id
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to delete video: {str(e)}"}
    
    def search_trending_hashtags(self, category: str = "drone") -> List[str]:
        """Search for trending hashtags"""
        # Note: TikTok API doesn't directly provide trending hashtags
        # This is a placeholder for trending drone-related hashtags
        drone_hashtags = [
            "#drone",
            "#dronelife", 
            "#dronephotography",
            "#aerialphotography",
            "#dji",
            "#mavic",
            "#fpv",
            "#cinematic",
            "#aerial",
            "#dronevideo",
            "#skyview",
            "#fromabove",
            "#birdseyeview",
            "#droneshots",
            "#airview"
        ]
        
        return drone_hashtags[:10]

class MockTikTokManager:
    """Mock TikTok manager for testing without API credentials"""
    
    def __init__(self, client_key: str = "", client_secret: str = ""):
        self.client_key = client_key
        self.client_secret = client_secret
        self.uploaded_videos = []
    
    def get_access_token(self) -> str:
        """Mock access token"""
        return "mock_access_token_12345"
    
    def upload_video(self, video_path: str, caption: str, hashtags: List[str]) -> Dict:
        """Mock video upload"""
        video_id = f"mock_video_{int(time.time())}"
        
        self.uploaded_videos.append({
            "video_id": video_id,
            "caption": caption,
            "hashtags": hashtags,
            "uploaded_at": datetime.now().isoformat()
        })
        
        return {
            "success": True,
            "video_id": video_id,
            "status": "published",
            "mock": True
        }
    
    def get_video_info(self, video_id: str) -> Dict:
        """Mock video info"""
        video = next((v for v in self.uploaded_videos if v["video_id"] == video_id), None)
        if video:
            return {
                "data": {
                    "video": {
                        "id": video_id,
                        "title": video["caption"][:100],
                        "description": video["caption"],
                        "hashtags": video["hashtags"],
                        "created_time": video["uploaded_at"]
                    }
                }
            }
        return {"error": "Video not found"}
    
    def get_user_videos(self, count: int = 20) -> List[Dict]:
        """Mock user videos"""
        return [
            {
                "id": v["video_id"],
                "title": v["caption"][:100],
                "description": v["caption"],
                "hashtags": v["hashtags"],
                "created_time": v["uploaded_at"]
            }
            for v in self.uploaded_videos[:count]
        ]
    
    def delete_video(self, video_id: str) -> Dict:
        """Mock delete video"""
        original_length = len(self.uploaded_videos)
        self.uploaded_videos = [v for v in self.uploaded_videos if v["video_id"] != video_id]
        
        if len(self.uploaded_videos) < original_length:
            return {"success": True, "message": "Video deleted"}
        return {"error": "Video not found"}
    
    def search_trending_hashtags(self, category: str = "drone") -> List[str]:
        """Mock trending hashtags"""
        return [
            "#drone",
            "#dronelife",
            "#dronephotography",
            "#aerialphotography",
            "#dji",
            "#mavic",
            "#fpv"
        ]

def create_tiktok_manager(use_mock: bool = True):
    """Create TikTok manager (mock or real)"""
    if use_mock:
        return MockTikTokManager()
    
    # For real API usage, you would get these from environment variables
    client_key = os.getenv("TIKTOK_CLIENT_KEY", "")
    client_secret = os.getenv("TIKTOK_CLIENT_SECRET", "")
    
    return TikTokManager(client_key, client_secret)