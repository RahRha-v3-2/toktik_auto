#!/usr/bin/env python3
"""
Automated Posting Scheduler for Drone Content
Handles scheduling and automated posting to TikTok
"""

import os
import json
import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

from drone_content_generator import DroneContentGenerator
from tiktok_manager import create_tiktok_manager
from video_processor import create_video_processor

class ContentScheduler:
    """Automated content posting scheduler"""
    
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.content_generator = None
        self.tiktok_manager = None
        self.video_processor = None
        
        # Initialize components
        self._initialize_components()
        
        # Load or create schedule
        self.schedule_file = "posting_schedule.json"
        self.content_queue = []
        self.posted_content = []
        
        self.load_schedule()
        
        # Default posting schedule
        self.default_schedule = {
            "morning": {"time": "08:00", "days": ["monday", "wednesday", "friday"]},
            "afternoon": {"time": "15:00", "days": ["tuesday", "thursday"]},
            "evening": {"time": "19:00", "days": ["saturday", "sunday"]}
        }
    
    def _initialize_components(self):
        """Initialize all components"""
        try:
            if not self.use_mock:
                # Initialize with API key for real usage
                api_key = os.getenv("GOOGLE_AI_API_KEY", "")
                if api_key:
                    self.content_generator = DroneContentGenerator(api_key)
                else:
                    print("Warning: No Google AI API key found, using mock")
                    self.use_mock = True
        except:
            self.use_mock = True
        
        # Always use mock generator as fallback
        if not self.content_generator:
            from mock_content_generator import MockContentGenerator
            self.content_generator = MockContentGenerator()
        
        self.tiktok_manager = create_tiktok_manager(self.use_mock)
        self.video_processor = create_video_processor(self.use_mock)
    
    def load_schedule(self):
        """Load posting schedule from file"""
        try:
            if os.path.exists(self.schedule_file):
                with open(self.schedule_file, 'r') as f:
                    data = json.load(f)
                    self.content_queue = data.get("queue", [])
                    self.posted_content = data.get("posted", [])
                print(f"Loaded schedule: {len(self.content_queue)} items in queue")
        except Exception as e:
            print(f"Error loading schedule: {e}")
            self.content_queue = []
            self.posted_content = []
    
    def save_schedule(self):
        """Save posting schedule to file"""
        try:
            data = {
                "queue": self.content_queue,
                "posted": self.posted_content,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.schedule_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print("Schedule saved successfully")
        except Exception as e:
            print(f"Error saving schedule: {e}")
    
    def generate_content_batch(self, count: int = 5) -> List[Dict]:
        """Generate a batch of content ideas and scripts"""
        batch_content = []
        
        if not self.content_generator:
            print("Content generator not available")
            return batch_content
        
        print(f"Generating {count} content items...")
        
        # Generate content ideas
        ideas = self.content_generator.generate_content_ideas("viral drone content", count)
        
        for i, idea in enumerate(ideas):
            try:
                # Generate script for each idea
                script = self.content_generator.generate_video_script(idea, "30 seconds")
                
                # Generate caption
                caption = self.content_generator.generate_caption(idea, "tiktok")
                
                # Get trending hashtags
                hashtags = self.tiktok_manager.search_trending_hashtags("drone")
                
                content_item = {
                    "id": f"content_{int(time.time())}_{i}",
                    "idea": idea,
                    "script": script,
                    "caption": caption,
                    "hashtags": hashtags[:5],  # Limit to 5 hashtags
                    "status": "ready",
                    "created_at": datetime.now().isoformat(),
                    "scheduled_for": None
                }
                
                batch_content.append(content_item)
                print(f"Generated content {i+1}: {idea[:50]}...")
                
            except Exception as e:
                print(f"Error generating content for idea {i}: {e}")
                continue
        
        return batch_content
    
    def add_to_queue(self, content_items: List[Dict]):
        """Add content items to posting queue"""
        for item in content_items:
            # Schedule random posting time within next 3 days
            days_ahead = random.randint(0, 3)
            hour = random.randint(8, 21)  # Post between 8 AM and 9 PM
            minute = random.choice([0, 15, 30, 45])  # Post at quarter hours
            
            scheduled_time = datetime.now() + timedelta(days=days_ahead)
            scheduled_time = scheduled_time.replace(hour=hour, minute=minute, second=0)
            
            item["scheduled_for"] = scheduled_time.isoformat()
            item["status"] = "scheduled"
            
            self.content_queue.append(item)
        
        self.save_schedule()
        print(f"Added {len(content_items)} items to posting queue")
    
    def process_queue(self):
        """Process the posting queue and post scheduled content"""
        now = datetime.now()
        posted_count = 0
        
        # Check each item in queue
        for item in self.content_queue[:]:  # Copy list to allow modification
            if item["status"] == "scheduled":
                scheduled_time = datetime.fromisoformat(item["scheduled_for"])
                
                if now >= scheduled_time:
                    print(f"Processing scheduled content: {item['idea'][:50]}...")
                    
                    result = self.post_content(item)
                    
                    if result.get("success"):
                        # Move to posted content
                        item["status"] = "posted"
                        item["posted_at"] = now.isoformat()
                        item["post_result"] = result
                        
                        self.posted_content.append(item)
                        self.content_queue.remove(item)
                        
                        posted_count += 1
                        print(f"Successfully posted content ID: {item['id']}")
                    else:
                        # Reschedule for later if failed
                        reschedule_time = now + timedelta(hours=2)
                        item["scheduled_for"] = reschedule_time.isoformat()
                        item["status"] = "failed"
                        
                        print(f"Failed to post content ID: {item['id']}, rescheduled")
        
        if posted_count > 0:
            self.save_schedule()
        
        return posted_count
    
    def post_content(self, content_item: Dict) -> Dict:
        """Post a single content item to TikTok"""
        try:
            # In a real implementation, you would:
            # 1. Generate or find the actual video file
            # 2. Process the video with video_processor
            # 3. Upload to TikTok with tiktok_manager
            
            # For mock implementation, simulate the process
            if self.use_mock:
                print(f"Mock posting: {content_item['caption']}")
                
                # Simulate processing steps
                video_path = f"mock_video_{content_item['id']}.mp4"
                
                # Mock video processing
                self.video_processor.resize_video(video_path, f"processed_{video_path}")
                self.video_processor.enhance_video(video_path, f"enhanced_{video_path}")
                self.video_processor.add_text_overlay(video_path, f"final_{video_path}", 
                                                     content_item['caption'][:20])
                
                # Mock upload
                result = self.tiktok_manager.upload_video(
                    video_path,
                    content_item["caption"],
                    content_item["hashtags"]
                )
                
                return {"success": True, "result": result}
            
            # Real implementation would go here
            return {"success": False, "error": "Real implementation not yet available"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def setup_schedule(self):
        """Setup automated posting schedule"""
        print("Setting up automated posting schedule...")
        
        # Schedule morning posts
        for day in self.default_schedule["morning"]["days"]:
            schedule.every().__getattribute__(day).at(self.default_schedule["morning"]["time"]).do(self.process_queue)
        
        # Schedule afternoon posts  
        for day in self.default_schedule["afternoon"]["days"]:
            schedule.every().__getattribute__(day).at(self.default_schedule["afternoon"]["time"]).do(self.process_queue)
        
        # Schedule evening posts
        for day in self.default_schedule["evening"]["days"]:
            schedule.every().__getattribute__(day).at(self.default_schedule["evening"]["time"]).do(self.process_queue)
        
        print("Schedule configured successfully")
    
    def run_scheduler(self):
        """Run the scheduler continuously"""
        print("Starting content scheduler...")
        
        # Setup the schedule
        self.setup_schedule()
        
        # Generate initial batch of content
        content_batch = self.generate_content_batch(3)
        self.add_to_queue(content_batch)
        
        print("Scheduler is running. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\nScheduler stopped by user")
            self.save_schedule()
    
    def get_queue_status(self) -> Dict:
        """Get current queue status"""
        now = datetime.now()
        
        scheduled_count = len([item for item in self.content_queue if item["status"] == "scheduled"])
        ready_count = len([item for item in self.content_queue if item["status"] == "ready"])
        posted_count = len(self.posted_content)
        
        # Find next scheduled post
        next_post = None
        for item in self.content_queue:
            if item["status"] == "scheduled":
                scheduled_time = datetime.fromisoformat(item["scheduled_for"])
                if scheduled_time > now:
                    next_post = item
                    break
        
        return {
            "total_in_queue": len(self.content_queue),
            "scheduled_count": scheduled_count,
            "ready_count": ready_count,
            "posted_count": posted_count,
            "next_post": next_post
        }
    
    def add_manual_post(self, idea: str, caption: str, hashtags: List[str], 
                       video_path: str) -> Dict:
        """Manually add a post to the queue"""
        content_item = {
            "id": f"manual_{int(time.time())}",
            "idea": idea,
            "caption": caption,
            "hashtags": hashtags,
            "video_path": video_path,
            "status": "ready",
            "created_at": datetime.now().isoformat(),
            "scheduled_for": None
        }
        
        self.content_queue.append(content_item)
        self.save_schedule()
        
        return {"success": True, "content_id": content_item["id"]}

def main():
    """Main function to run the scheduler"""
    print("🚁 TikTok Drone Content Scheduler")
    print("=" * 50)
    
    # Create scheduler (use mock for demo)
    scheduler = ContentScheduler(use_mock=True)
    
    # Show current status
    status = scheduler.get_queue_status()
    print(f"\n📊 Queue Status:")
    print(f"  Items in queue: {status['total_in_queue']}")
    print(f"  Scheduled: {status['scheduled_count']}")
    print(f"  Ready: {status['ready_count']}")
    print(f"  Posted: {status['posted_count']}")
    
    if status['next_post']:
        next_time = datetime.fromisoformat(status['next_post']['scheduled_for'])
        print(f"  Next post: {next_time.strftime('%Y-%m-%d %H:%M')}")
    
    # Demo: Generate and add content
    print(f"\n🎯 Generating demo content...")
    content_batch = scheduler.generate_content_batch(2)
    
    if content_batch:
        scheduler.add_to_queue(content_batch)
        
        # Process queue immediately for demo
        print(f"\n📤 Processing queue...")
        posted = scheduler.process_queue()
        print(f"Posted {posted} items")
    
    # Show final status
    final_status = scheduler.get_queue_status()
    print(f"\n📊 Final Status:")
    print(f"  Items in queue: {final_status['total_in_queue']}")
    print(f"  Posted: {final_status['posted_count']}")
    
    print(f"\n✅ Demo completed!")

if __name__ == "__main__":
    main()