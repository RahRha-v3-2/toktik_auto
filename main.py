#!/usr/bin/env python3
"""
Main Application - TikTok Drone Content Generator
Complete system for generating and managing drone content for TikTok
"""

import os
import sys
import argparse
from datetime import datetime
import json

from drone_content_generator import DroneContentGenerator
from tiktok_manager import create_tiktok_manager
from video_processor import create_video_processor
from content_scheduler import ContentScheduler

class TikTokDroneApp:
    """Main application class"""
    
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.content_generator = None
        self.tiktok_manager = None
        self.video_processor = None
        self.scheduler = None
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all components"""
        print("🚁 Initializing TikTok Drone Content Generator...")
        
        try:
            if not self.use_mock:
                # Try to initialize with real API keys
                google_api_key = os.getenv("GOOGLE_AI_API_KEY")
                if google_api_key:
                    self.content_generator = DroneContentGenerator(google_api_key)
                    print("✅ Google AI connected")
                else:
                    print("⚠️  No Google AI API key found, using mock mode")
                    self.use_mock = True
        except Exception as e:
            print(f"⚠️  Error initializing content generator: {e}")
            self.use_mock = True
        
        # Always use mock generator as fallback
        if not self.content_generator:
            from mock_content_generator import MockContentGenerator
            self.content_generator = MockContentGenerator()
            print("✅ Using mock content generator")
        
        self.tiktok_manager = create_tiktok_manager(self.use_mock)
        self.video_processor = create_video_processor(self.use_mock)
        self.scheduler = ContentScheduler(self.use_mock)
        
        print(f"✅ Components initialized (Mock mode: {self.use_mock})")
    
    def generate_content(self, theme: str = "viral drone content", count: int = 5):
        """Generate content ideas and scripts"""
        print(f"\n🎯 Generating {count} content ideas for theme: '{theme}'")
        
        if not self.content_generator:
            print("❌ Content generator not available")
            return []
        
        try:
            ideas = self.content_generator.generate_content_ideas(theme, count)
            print(f"✅ Generated {len(ideas)} content ideas:")
            
            content_list = []
            for i, idea in enumerate(ideas, 1):
                print(f"{i}. {idea}")
                
                # Generate script and caption
                script = self.content_generator.generate_video_script(idea)
                caption = self.content_generator.generate_caption(idea, "tiktok")
                
                content = {
                    "id": f"content_{int(datetime.now().timestamp())}_{i}",
                    "idea": idea,
                    "script": script,
                    "caption": caption,
                    "created_at": datetime.now().isoformat()
                }
                content_list.append(content)
            
            return content_list
            
        except Exception as e:
            print(f"❌ Error generating content: {e}")
            return []
    
    def analyze_trends(self):
        """Analyze trending drone content"""
        print("\n📈 Analyzing trending drone content...")
        
        if not self.content_generator:
            print("❌ Content generator not available")
            return
        
        try:
            trends = self.content_generator.analyze_trending_drone_content()
            print("✅ Trend Analysis:")
            
            if isinstance(trends, dict) and "analysis" in trends:
                print(trends["analysis"])
            else:
                print(json.dumps(trends, indent=2))
                
        except Exception as e:
            print(f"❌ Error analyzing trends: {e}")
    
    def get_hashtags(self, category: str = "drone"):
        """Get trending hashtags"""
        print(f"\n#️⃣ Getting trending hashtags for '{category}'...")
        
        try:
            hashtags = self.tiktok_manager.search_trending_hashtags(category)
            print(f"✅ Found {len(hashtags)} trending hashtags:")
            
            for i, hashtag in enumerate(hashtags[:10], 1):
                print(f"{i}. {hashtag}")
            
            return hashtags
            
        except Exception as e:
            print(f"❌ Error getting hashtags: {e}")
            return []
    
    def simulate_posting(self, content_list):
        """Simulate posting content to TikTok"""
        print(f"\n📤 Simulating posting {len(content_list)} items...")
        
        posted_items = []
        
        for i, content in enumerate(content_list, 1):
            print(f"\nPosting item {i}/{len(content_list)}")
            print(f"Idea: {content['idea'][:50]}...")
            
            # Get hashtags
            hashtags = self.get_hashtags()
            
            # Simulate video processing
            print("Processing video...")
            mock_video_path = f"drone_video_{content['id']}.mp4"
            
            if self.video_processor:
                self.video_processor.resize_video(mock_video_path, f"processed_{mock_video_path}")
                self.video_processor.enhance_video(mock_video_path, f"enhanced_{mock_video_path}")
            
            # Simulate upload
            print("Uploading to TikTok...")
            result = self.tiktok_manager.upload_video(
                mock_video_path,
                content['caption'],
                hashtags[:5]
            )
            
            if result.get("success"):
                print(f"✅ Posted successfully! Video ID: {result.get('video_id')}")
                posted_items.append({
                    **content,
                    "post_result": result,
                    "posted_at": datetime.now().isoformat()
                })
            else:
                print(f"❌ Posting failed: {result.get('error')}")
        
        return posted_items
    
    def show_queue_status(self):
        """Show current queue status"""
        print("\n📊 Queue Status:")
        
        status = self.scheduler.get_queue_status()
        
        print(f"  📋 Items in queue: {status['total_in_queue']}")
        print(f"  ⏰ Scheduled: {status['scheduled_count']}")
        print(f"  ✅ Ready: {status['ready_count']}")
        print(f"  📤 Posted: {status['posted_count']}")
        
        if status['next_post']:
            next_time = datetime.fromisoformat(status['next_post']['scheduled_for'])
            print(f"  🎯 Next post: {next_time.strftime('%Y-%m-%d %H:%M')} - {status['next_post']['idea'][:30]}...")
    
    def run_scheduler_demo(self):
        """Run scheduler demo"""
        print("\n🚀 Running Scheduler Demo")
        print("=" * 50)
        
        # Show current status
        self.show_queue_status()
        
        # Generate content and add to queue
        print("\n🎯 Generating content for queue...")
        content_batch = self.scheduler.generate_content_batch(3)
        
        if content_batch:
            self.scheduler.add_to_queue(content_batch)
            print(f"✅ Added {len(content_batch)} items to queue")
            
            # Process queue
            print("\n📤 Processing queue...")
            posted = self.scheduler.process_queue()
            print(f"✅ Posted {posted} items")
        
        # Show final status
        self.show_queue_status()
    
    def interactive_mode(self):
        """Interactive command-line mode"""
        print("\n🎮 Interactive Mode")
        print("Available commands:")
        print("  generate <count> - Generate content ideas")
        print("  trends - Analyze trending content")
        print("  hashtags - Get trending hashtags")
        print("  queue - Show queue status")
        print("  post - Simulate posting")
        print("  scheduler - Run scheduler demo")
        print("  quit - Exit")
        
        while True:
            try:
                command = input("\n🚁 Enter command: ").strip().lower()
                
                if not command:
                    continue
                
                if command == "quit" or command == "exit":
                    print("👋 Goodbye!")
                    break
                elif command.startswith("generate"):
                    parts = command.split()
                    count = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5
                    self.generate_content(count=count)
                elif command == "trends":
                    self.analyze_trends()
                elif command == "hashtags":
                    self.get_hashtags()
                elif command == "queue":
                    self.show_queue_status()
                elif command == "post":
                    content = self.generate_content(count=2)
                    if content:
                        self.simulate_posting(content)
                elif command == "scheduler":
                    self.run_scheduler_demo()
                else:
                    print("❌ Unknown command. Try: generate, trends, hashtags, queue, post, scheduler, quit")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="TikTok Drone Content Generator")
    parser.add_argument("--mock", action="store_true", default=True, help="Use mock mode (default)")
    parser.add_argument("--real", action="store_true", help="Use real API integration")
    parser.add_argument("--generate", type=int, metavar="COUNT", help="Generate COUNT content ideas")
    parser.add_argument("--trends", action="store_true", help="Analyze trending content")
    parser.add_argument("--hashtags", action="store_true", help="Get trending hashtags")
    parser.add_argument("--scheduler", action="store_true", help="Run scheduler demo")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    # Determine mode
    use_mock = not args.real
    
    # Create app
    app = TikTokDroneApp(use_mock=use_mock)
    
    # Handle commands
    if args.interactive:
        app.interactive_mode()
    elif args.scheduler:
        app.run_scheduler_demo()
    elif args.trends:
        app.analyze_trends()
    elif args.hashtags:
        app.get_hashtags()
    elif args.generate:
        content = app.generate_content(count=args.generate)
        if content:
            app.simulate_posting(content)
    else:
        # Default demo mode
        print("\n🎬 Running Demo Mode")
        print("=" * 50)
        
        # Generate content
        content = app.generate_content(count=3)
        
        # Get hashtags
        hashtags = app.get_hashtags()
        
        # Simulate posting
        if content:
            app.simulate_posting(content)
        
        # Show queue status
        app.show_queue_status()
        
        print("\n✅ Demo completed!")

if __name__ == "__main__":
    main()