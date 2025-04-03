from pathlib import Path
import os
import sys
import time
import traceback
import requests
import urllib.request
from pydub import AudioSegment
import moviepy.editor as mp
from PIL import Image
import numpy as np

def find_effects():
    """Find all video effect overlays in the effects directory"""
    print("Finding video effects...")
    effects_dir = Path(__file__).parent.parent / "assets/effects"
    effects_dir.mkdir(parents=True, exist_ok=True)
    
    # Look for video files with common video extensions
    video_extensions = ['.mp4', '.mov', '.avi', '.webm']
    effect_files = []
    
    for ext in video_extensions:
        effect_files.extend(list(effects_dir.glob(f"*{ext}")))
    
    if effect_files:
        print(f"Found {len(effect_files)} effect files:")
        for effect in effect_files:
            print(f"- {effect.name}")
        return effect_files
    else:
        print("No effect files found in the effects directory.")
        print(f"Please add effect videos to: {effects_dir.resolve()}")
        print("Check the README in the effects directory for instructions.")
        return []

def download_fire_effect():
    """Download fire effect overlay if it doesn't exist already"""
    print("Checking for fire effect overlay...")
    effects_dir = Path(__file__).parent.parent / "assets/effects"
    effects_dir.mkdir(parents=True, exist_ok=True)
    
    fire_effect_path = effects_dir / "fire_overlay.mp4"
    
    if fire_effect_path.exists():
        print(f"Fire effect already exists at: {fire_effect_path}")
        return fire_effect_path
    
    # URL to a free fire overlay effect with transparent background
    # Note: In a real scenario, you would need to ensure you have proper licensing for the effect
    # This is just a placeholder - users should replace with their own fire overlay
    fire_effect_url = "https://example.com/fire_overlay.mp4"  # Replace with actual URL to fire effect
    
    try:
        print(f"Downloading fire effect from {fire_effect_url}...")
        # For manual download instructions (since we can't directly download in this example)
        print("NOTE: Automatic download not available in this script.")
        print("Please download a fire overlay video with alpha channel/transparent background")
        print(f"and save it to: {fire_effect_path}")
        print("You can find free fire overlay videos on sites like:")
        print("- Videezy.com (search for 'fire overlay with alpha channel')")
        print("- Pexels.com")
        print("- Pixabay.com")
        
        # Placeholder for downloaded fire effect
        if not fire_effect_path.exists():
            print("Using a placeholder path for demonstration purposes.")
            # Return the path even if it doesn't exist yet - user will need to manually download
        
        return fire_effect_path
    except Exception as e:
        print(f"Error downloading fire effect: {e}")
        traceback.print_exc()
        return None

def find_latest_files():
    print("Finding latest generated files...")
    try:
        # Find latest speech file
        speeches_dir = Path(__file__).parent.parent / "results/speeches"
        print(f"Looking for speech files in: {speeches_dir.resolve()}")
        speech_files = list(speeches_dir.glob("speech_*.mp3"))
        if not speech_files:
            print("No speech files found.")
            return None, None
        latest_speech = max(speech_files, key=lambda x: int(x.stem.split('_')[1]))
        
        # Find latest image file
        images_dir = Path(__file__).parent.parent / "results/images"
        image_files = list(images_dir.glob("image_*.png"))
        if not image_files:
            # Try character_reference.png if no numbered images found
            character_ref = images_dir / "character_reference.png"
            if character_ref.exists():
                latest_image = character_ref
            else:
                print("No image files found.")
                return latest_speech, None
        else:
            latest_image = max(image_files, key=lambda x: int(x.stem.split('_')[1]))
        
        print(f"Found latest speech: {latest_speech}")
        print(f"Found latest image: {latest_image}")
        
        return latest_speech, latest_image
    except Exception as e:
        print(f"Error finding latest files: {e}")
        traceback.print_exc()
        return None, None

def apply_grow_and_turn_effect(clip, total_duration, animation_duration=2.0):
    """Apply a grow and turn effect (similar to PowerPoint) to the clip"""
    print("Applying grow and turn effect to image...")
    
    # Define the animation duration (in seconds)
    # If animation_duration is too long compared to total_duration, reduce it
    if animation_duration > total_duration / 3:
        animation_duration = total_duration / 3
    
    # For grow effect, we'll use a resize function that changes with time
    def grow_effect(t):
        if t < animation_duration:
            progress = t / animation_duration  # 0 to 1 during animation
            scale = 0.5 + 0.5 * progress  # Start at 0.5x size, end at 1x size
            return scale
        else:
            return 1.0  # Full size after animation
    
    # For rotation effect, we'll use a rotate function that changes with time
    def rotate_effect(t):
        if t < animation_duration:
            progress = t / animation_duration  # 0 to 1 during animation
            angle = 360 * progress  # Full rotation during animation
            return angle
        else:
            return 0  # No rotation after animation
    
    # Apply custom effects in sequence
    # First apply dynamic resizing
    resized_clip = clip.fx(mp.vfx.resize, lambda t: grow_effect(t))
    
    # Then apply rotation
    final_clip = resized_clip.fx(mp.vfx.rotate, lambda t: rotate_effect(t))
    
    return final_clip

def create_video(image_path, audio_path, output_path, effect_paths=None, use_grow_and_turn=True):
    """Create a video with the image, audio, and all video effects"""
    print("Creating video...")
    try:
        # Get audio duration
        audio = AudioSegment.from_file(str(audio_path))
        total_duration = len(audio) / 1000.0  # Convert to seconds
        
        print(f"Audio duration: {total_duration:.2f} seconds")
        
        # Load the image
        img = Image.open(image_path)
        img_w, img_h = img.size
        
        # Target dimensions for the video (portrait orientation)
        target_width = 1080
        target_height = 1920
        
        # Create the background image clip
        image_clip = (mp.ImageClip(str(image_path))
                      .set_duration(total_duration))
        
        # Calculate scaling to fit the image within the target dimensions
        # while maintaining aspect ratio and adding black bars where needed
        width_ratio = target_width / img_w
        height_ratio = target_height / img_h
        
        # Use the smaller ratio to ensure the image fits completely
        scale_factor = min(width_ratio, height_ratio)
        
        # Calculate new dimensions
        new_width = int(img_w * scale_factor)
        new_height = int(img_h * scale_factor)
        
        # Resize the image while maintaining aspect ratio
        image_clip = image_clip.resize(width=new_width, height=new_height)
        
        # Apply grow and turn effect if requested
        if use_grow_and_turn:
            image_clip = apply_grow_and_turn_effect(image_clip, total_duration)
        
        # Center the image on the black background
        image_clip = image_clip.set_position(('center', 'center'))
        
        # Create black background
        bg_clip = mp.ColorClip(size=(target_width, target_height), color=(0, 0, 0))
        bg_clip = bg_clip.set_duration(total_duration)
        
        # List to hold all clips
        clips = [bg_clip, image_clip]
        
        # Add effects if available
        if effect_paths:
            for idx, effect_path in enumerate(effect_paths):
                if effect_path.exists():
                    try:
                        print(f"Adding effect from: {effect_path}")
                        
                        # Load the effect
                        effect_clip = mp.VideoFileClip(str(effect_path))
                        
                        # Make it loop for the duration of our video if it's shorter
                        if effect_clip.duration < total_duration:
                            effect_clip = effect_clip.fx(mp.vfx.loop, duration=total_duration)
                        else:
                            # Trim if it's longer than our video
                            effect_clip = effect_clip.subclip(0, total_duration)
                        
                        # Scale to cover the entire frame
                        effect_clip = effect_clip.resize(height=target_height)
                        if effect_clip.w < target_width:
                            effect_clip = effect_clip.resize(width=target_width)
                        
                        # Center the effect
                        effect_clip = effect_clip.set_position(('center', 'center'))
                        
                        # Use a blending mode suitable for overlays
                        # Adjust opacity based on the effect number - later effects are slightly more transparent
                        # This helps when layering multiple effects
                        base_opacity = 0.4
                        opacity_reduction = 0.05 * idx  # Reduce opacity slightly for each additional effect
                        final_opacity = max(0.2, base_opacity - opacity_reduction)  # Don't go below 0.2
                        
                        effect_clip = effect_clip.set_opacity(final_opacity)
                        
                        # Add the effect clip on top of the other clips
                        clips.append(effect_clip)
                        
                        print(f"Effect '{effect_path.name}' added successfully with opacity {final_opacity:.2f}")
                    except Exception as e:
                        print(f"Error adding effect {effect_path}: {e}. Skipping this effect.")
                        traceback.print_exc()
            
        # Combine all clips
        video = mp.CompositeVideoClip(clips, size=(target_width, target_height))
        
        # Add audio
        audio_clip = mp.AudioFileClip(str(audio_path))
        video = video.set_audio(audio_clip)
        
        # Write the video file
        print(f"Writing video to {output_path}...")
        video.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            bitrate='5000k',
            audio_bitrate='192k',
            threads=4
        )
        
        # Properly close all clips to avoid FFMPEG errors
        video.close()
        audio_clip.close()
        image_clip.close()
        bg_clip.close()
        
        # Close any effect clips
        if effect_paths:
            for clip in clips[2:]:  # Skip bg_clip and image_clip which are already closed
                try:
                    clip.close()
                except:
                    pass
        
        print(f"Video created successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error creating video: {e}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    try:
        # Make sure necessary directories exist
        output_dir = Path(__file__).parent.parent / "results/videos"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n" + "="*50)
        print("STEP 1: FINDING LATEST GENERATED FILES")
        print("="*50)
        speech_file, image_file = find_latest_files()
        
        if not speech_file or not image_file:
            print("Missing required files. Exiting.")
            sys.exit(1)
        
        print("\n" + "="*50)
        print("STEP 2: FINDING VIDEO EFFECTS")
        print("="*50)
        effect_paths = find_effects()
        
        # If no effects found, check for fire effect as fallback
        if not effect_paths:
            print("No effects found. Checking for fire effect...")
            fire_effect_path = download_fire_effect()
            if fire_effect_path and fire_effect_path.exists():
                effect_paths = [fire_effect_path]
            
        # Create output video path
        video_files = list(output_dir.glob("video_*.mp4"))
        next_number = len(video_files) + 1 if video_files else 1
        output_path = output_dir / f"video_{next_number}.mp4"
        
        # Ask if grow and turn effect should be used
        use_grow_and_turn = True  # Default to using the effect
        
        print("\n" + "="*50)
        print("STEP 3: CREATING VIDEO WITH EFFECTS")
        print("="*50)
        print("Applying grow and turn effect to image: Yes")
        video_path = create_video(image_file, speech_file, output_path, effect_paths, use_grow_and_turn)
        
        if not video_path:
            print("Failed to create video. Exiting.")
            sys.exit(1)
        
        print("\n" + "="*50)
        print("VIDEO CREATION COMPLETE!")
        print("="*50)
        print(f"Video saved to: {video_path}")
        print(f"Number of effects applied: {len(effect_paths)} overlay(s) + grow and turn effect")
        print("="*50 + "\n")
        
        # Ensure console output is fully displayed before exiting
        sys.stdout.flush()
        time.sleep(1)
        
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        traceback.print_exc()
        sys.exit(1) 