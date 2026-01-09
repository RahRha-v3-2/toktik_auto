#!/usr/bin/env python3
"""
Video Processing Module for Drone Content
Handles video editing, enhancement, and formatting for TikTok
"""

import os
from typing import List, Dict, Optional, Tuple
import subprocess
from datetime import datetime
import tempfile

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageEnhance, ImageFilter
    VIDEO_PROCESSING_AVAILABLE = True
except ImportError:
    VIDEO_PROCESSING_AVAILABLE = False

class VideoProcessor:
    """Video processing and editing for drone content"""
    
    def __init__(self):
        if not VIDEO_PROCESSING_AVAILABLE:
            raise ImportError("Video processing libraries not available")
        self.temp_dir = tempfile.mkdtemp()
        print(f"Using temp directory: {self.temp_dir}")
    
    def __del__(self):
        """Clean up temp files"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass
    
    def resize_video(self, input_path: str, output_path: str, 
                    width: int = 1080, height: int = 1920) -> bool:
        """Resize video to TikTok vertical format (9:16)"""
        if not VIDEO_PROCESSING_AVAILABLE:
            return False
            
        try:
            cap = cv2.VideoCapture(input_path)
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Resize frame maintaining aspect ratio
                frame_height, frame_width = frame.shape[:2]
                aspect_ratio = frame_width / frame_height
                
                if aspect_ratio > 9/16:  # Wider than 9:16
                    new_width = int(height * aspect_ratio)
                    resized = cv2.resize(frame, (new_width, height))
                    # Crop center
                    start_x = (new_width - width) // 2
                    cropped = resized[:, start_x:start_x + width]
                else:  # Taller than 9:16
                    new_height = int(width / aspect_ratio)
                    resized = cv2.resize(frame, (width, new_height))
                    # Add black bars top/bottom
                    top_bottom = (height - new_height) // 2
                    cropped = np.zeros((height, width, 3), dtype=np.uint8)
                    cropped[top_bottom:top_bottom + new_height, :] = resized
                
                out.write(cropped)
                frame_count += 1
                
                if frame_count % 100 == 0:
                    print(f"Processed {frame_count}/{total_frames} frames")
            
            cap.release()
            out.release()
            
            print(f"Video resized successfully: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error resizing video: {e}")
            return False
    
    def add_music(self, video_path: str, audio_path: str, output_path: str) -> bool:
        """Add background music to video"""
        try:
            # Use ffmpeg for audio mixing
            cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-shortest',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Audio added successfully: {output_path}")
                return True
            else:
                print(f"FFmpeg error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error adding music: {e}")
            return False
    
    def trim_video(self, input_path: str, output_path: str, 
                  start_time: float, duration: float) -> bool:
        """Trim video to specific duration"""
        try:
            cap = cv2.VideoCapture(input_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()
            
            start_frame = int(start_time * fps)
            end_frame = int((start_time + duration) * fps)
            
            # Use ffmpeg for trimming
            cmd = [
                'ffmpeg', '-y',
                '-i', input_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c', 'copy',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Video trimmed successfully: {output_path}")
                return True
            else:
                print(f"FFmpeg error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error trimming video: {e}")
            return False
    
    def enhance_video(self, input_path: str, output_path: str, 
                     brightness: float = 1.2, 
                     contrast: float = 1.1,
                     saturation: float = 1.1) -> bool:
        """Enhance video quality with filters"""
        try:
            cap = cv2.VideoCapture(input_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Convert to PIL for enhancement
                pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                
                # Apply enhancements
                if brightness != 1.0:
                    enhancer = ImageEnhance.Brightness(pil_image)
                    pil_image = enhancer.enhance(brightness)
                
                if contrast != 1.0:
                    enhancer = ImageEnhance.Contrast(pil_image)
                    pil_image = enhancer.enhance(contrast)
                
                if saturation != 1.0:
                    enhancer = ImageEnhance.Color(pil_image)
                    pil_image = enhancer.enhance(saturation)
                
                # Convert back to OpenCV
                enhanced_frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                out.write(enhanced_frame)
                
                frame_count += 1
                if frame_count % 100 == 0:
                    print(f"Enhanced {frame_count} frames")
            
            cap.release()
            out.release()
            
            print(f"Video enhanced successfully: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error enhancing video: {e}")
            return False
    
    def add_text_overlay(self, input_path: str, output_path: str, 
                       text: str, position: str = "bottom") -> bool:
        """Add text overlay to video"""
        try:
            cap = cv2.VideoCapture(input_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            # Text settings
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2
            text_color = (255, 255, 255)  # White
            background_color = (0, 0, 0)  # Black
            
            # Calculate text position
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            
            if position == "bottom":
                text_x = (width - text_size[0]) // 2
                text_y = height - 50
            elif position == "top":
                text_x = (width - text_size[0]) // 2
                text_y = 50
            else:  # center
                text_x = (width - text_size[0]) // 2
                text_y = height // 2
            
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Add background rectangle
                cv2.rectangle(frame, 
                            (text_x - 10, text_y - text_size[1] - 10),
                            (text_x + text_size[0] + 10, text_y + 10),
                            background_color, -1)
                
                # Add text
                cv2.putText(frame, text, (text_x, text_y), 
                           font, font_scale, text_color, thickness)
                
                out.write(frame)
                frame_count += 1
                
                if frame_count % 100 == 0:
                    print(f"Processed {frame_count} frames with text")
            
            cap.release()
            out.release()
            
            print(f"Text overlay added successfully: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error adding text overlay: {e}")
            return False
    
    def create_cinematic_effect(self, input_path: str, output_path: str) -> bool:
        """Add cinematic look to drone footage"""
        try:
            cap = cv2.VideoCapture(input_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Convert to float for processing
                frame_float = frame.astype(np.float32) / 255.0
                
                # Apply cinematic LUT (color grading)
                # Increase contrast, slightly desaturate, add blue tint
                frame_float = frame_float ** 1.1  # Gamma correction
                frame_float[:, :, 0] *= 0.9  # Reduce red
                frame_float[:, :, 1] *= 0.95  # Slightly reduce green
                frame_float[:, :, 2] *= 1.1   # Increase blue
                
                # Add subtle vignette
                rows, cols = frame_float.shape[:2]
                X_resultant_kernel = cv2.getGaussianKernel(cols, cols/2)
                Y_resultant_kernel = cv2.getGaussianKernel(rows, rows/2)
                kernel = Y_resultant_kernel * X_resultant_kernel.T
                mask = kernel / np.linalg.norm(kernel)
                
                vignette = np.dstack([mask] * 3)
                frame_float = frame_float * vignette * 0.7 + frame_float * 0.3
                
                # Convert back to uint8
                processed_frame = np.clip(frame_float * 255, 0, 255).astype(np.uint8)
                
                out.write(processed_frame)
                frame_count += 1
                
                if frame_count % 100 == 0:
                    print(f"Processed {frame_count} frames with cinematic effect")
            
            cap.release()
            out.release()
            
            print(f"Cinematic effect applied successfully: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error applying cinematic effect: {e}")
            return False
    
    def generate_video_thumbnail(self, video_path: str, output_path: str, 
                                timestamp: float = 1.0) -> bool:
        """Generate thumbnail from video"""
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_number = int(timestamp * fps)
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            
            if ret:
                cv2.imwrite(output_path, frame)
                print(f"Thumbnail generated: {output_path}")
                return True
            else:
                print(f"Failed to extract frame at timestamp {timestamp}")
                return False
                
        except Exception as e:
            print(f"Error generating thumbnail: {e}")
            return False
        finally:
            cap.release()
    
    def get_video_info(self, video_path: str) -> Dict:
        """Get video metadata"""
        try:
            cap = cv2.VideoCapture(video_path)
            
            info = {
                "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "fps": cap.get(cv2.CAP_PROP_FPS),
                "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                "duration": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)
            }
            
            cap.release()
            return info
            
        except Exception as e:
            print(f"Error getting video info: {e}")
            return {}

class MockVideoProcessor:
    """Mock video processor for testing without actual video files"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        print(f"Mock video processor using temp directory: {self.temp_dir}")
    
    def resize_video(self, input_path: str, output_path: str, 
                    width: int = 1080, height: int = 1920) -> bool:
        print(f"Mock: Resizing {input_path} -> {output_path} ({width}x{height})")
        return True
    
    def add_music(self, video_path: str, audio_path: str, output_path: str) -> bool:
        print(f"Mock: Adding music {audio_path} to {video_path} -> {output_path}")
        return True
    
    def trim_video(self, input_path: str, output_path: str, 
                  start_time: float, duration: float) -> bool:
        print(f"Mock: Trimming {input_path} ({start_time}s, {duration}s) -> {output_path}")
        return True
    
    def enhance_video(self, input_path: str, output_path: str, 
                     brightness: float = 1.2, contrast: float = 1.1,
                     saturation: float = 1.1) -> bool:
        print(f"Mock: Enhancing {input_path} -> {output_path}")
        return True
    
    def add_text_overlay(self, input_path: str, output_path: str, 
                        text: str, position: str = "bottom") -> bool:
        print(f"Mock: Adding text '{text}' to {input_path} -> {output_path}")
        return True
    
    def create_cinematic_effect(self, input_path: str, output_path: str) -> bool:
        print(f"Mock: Adding cinematic effect to {input_path} -> {output_path}")
        return True
    
    def generate_video_thumbnail(self, video_path: str, output_path: str, 
                                timestamp: float = 1.0) -> bool:
        print(f"Mock: Generating thumbnail from {video_path} -> {output_path}")
        return True
    
    def get_video_info(self, video_path: str) -> Dict:
        return {
            "width": 1080,
            "height": 1920,
            "fps": 30,
            "frame_count": 900,
            "duration": 30.0,
            "mock": True
        }

def create_video_processor(use_mock: bool = True):
    """Create video processor (mock or real)"""
    if use_mock:
        return MockVideoProcessor()
    
    try:
        # Check if cv2 is available
        import cv2
        return VideoProcessor()
    except ImportError:
        print("OpenCV not available, using mock processor")
        return MockVideoProcessor()