# TikTok Drone Content Generator

🚁 Complete system for generating and managing drone content for TikTok

## Overview

This automated system generates viral drone video content ideas, creates scripts, manages TikTok posting, and handles video processing - all designed to grow your TikTok drone channel.

## Features

### 🎯 Content Generation
- Generate viral drone video ideas
- Create detailed video scripts
- Generate engaging TikTok captions
- Analyze trending drone content patterns
- Get trending hashtags for drone content

### 📹 Video Processing  
- Resize videos to TikTok format (9:16)
- Add cinematic effects and enhancements
- Add text overlays and watermarks
- Generate thumbnails
- Trim and edit videos

### 📤 TikTok Integration
- Upload videos directly to TikTok
- Manage posted content
- Schedule posts for optimal times
- Track posting history

### ⏰ Automated Scheduling
- Set up posting schedules
- Queue multiple posts
- Automated content generation
- Batch processing capabilities

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd toktik_auto
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Demo Mode (Mock)
Run the complete demo to see all features:
```bash
python3 main.py
```

Generate content ideas:
```bash
python3 main.py --generate 5
```

Run scheduler demo:
```bash
python3 main.py --scheduler
```

### Interactive Mode
For hands-on exploration:
```bash
python3 main.py --interactive
```

## Usage Options

### Command Line Arguments

- `--mock`: Use mock mode (default)
- `--real`: Use real API integration
- `--generate N`: Generate N content ideas
- `--trends`: Analyze trending content
- `--hashtags`: Get trending hashtags
- `--scheduler`: Run scheduler demo
- `--interactive`: Interactive command-line mode

### Examples

```bash
# Generate 3 viral drone ideas
python3 main.py --generate 3

# Analyze current trends
python3 main.py --trends

# Get trending hashtags
python3 main.py --hashtags

# Run interactive mode
python3 main.py --interactive
```

## Real API Integration

To use real APIs instead of mock mode:

1. Set environment variables:
```bash
export GOOGLE_AI_API_KEY="your-google-ai-api-key"
export TIKTOK_CLIENT_KEY="your-tiktok-client-key"
export TIKTOK_CLIENT_SECRET="your-tiktok-client-secret"
```

2. Run with real mode:
```bash
python3 main.py --real --generate 5
```

## Component Overview

### Files Structure

- `main.py` - Main application interface
- `drone_content_generator.py` - Google AI content generation
- `tiktok_manager.py` - TikTok API integration
- `video_processor.py` - Video editing and processing
- `content_scheduler.py` - Automated posting scheduler
- `mock_content_generator.py` - Mock content generator for testing

### Key Classes

- **TikTokDroneApp**: Main application controller
- **DroneContentGenerator**: AI-powered content creation
- **TikTokManager**: TikTok API management
- **VideoProcessor**: Video editing capabilities
- **ContentScheduler**: Automated posting system

## Mock vs Real Mode

### Mock Mode (Default)
- ✅ Works without API keys
- ✅ Safe for testing and development
- ✅ Demonstrates all features
- ❌ No real API calls

### Real Mode
- ✅ Actual content generation via Google AI
- ✅ Real TikTok API integration
- ✅ Actual video processing
- ❌ Requires API keys and quotas

## Scheduling

The system supports automated posting with customizable schedules:

### Default Schedule
- **Morning**: 8:00 AM (Mon, Wed, Fri)
- **Afternoon**: 3:00 PM (Tue, Thu)  
- **Evening**: 7:00 PM (Sat, Sun)

### Content Queue Management
- Generate content batches
- Schedule posts automatically
- Track posting history
- Reschedule failed posts

## Video Processing Features

### Supported Operations
- Resize to TikTok vertical format (1080x1920)
- Brightness, contrast, saturation adjustments
- Cinematic color grading
- Text overlay with custom positioning
- Thumbnail generation
- Video trimming

### Processing Pipeline
1. Original drone footage
2. Resize to 9:16 format
3. Apply cinematic enhancements
4. Add text overlay
5. Generate thumbnail
6. Upload to TikTok

## API Integration Notes

### Google AI Studio
- Uses Gemini 2.0 Flash model
- Generates creative content ideas
- Creates engaging captions
- Analyzes trends

### TikTok API
- OAuth 2.0 authentication
- Video upload and publishing
- Content management
- Hashtag research

## Troubleshooting

### Common Issues

**Import Errors**: Install missing dependencies
```bash
pip install -r requirements.txt
```

**API Quota Limits**: Use mock mode for testing
```bash
python3 main.py --mock
```

**Video Processing**: Install FFmpeg for enhanced processing
```bash
# On Ubuntu/Debian
sudo apt-get install ffmpeg

# On macOS
brew install ffmpeg
```

## Development

### Adding New Features

1. **New Content Types**: Extend `DroneContentGenerator`
2. **Additional Platforms**: Create platform managers
3. **Advanced Effects**: Enhance `VideoProcessor`
4. **Custom Schedules**: Modify `ContentScheduler`

### Testing

Run comprehensive tests:
```bash
python3 -m pytest tests/
```

Mock mode is recommended for development and testing.

## License

This project is for educational and development purposes. Ensure compliance with TikTok's terms of service and API usage policies.

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## Support

For issues and questions:
1. Check this README
2. Review code comments
3. Test with mock mode first
4. Verify API key configuration