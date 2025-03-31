from pathlib import Path
import os
import sys
import time
import traceback
from pydub import AudioSegment
import moviepy.editor as mp
from PIL import Image

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

def create_video(image_path, audio_path, output_path):
    """Create a video with the image and audio (no subtitles)"""
    print("Creating video...")
    try:
        # Get audio duration
        audio = AudioSegment.from_file(str(audio_path))
        total_duration = len(audio) / 1000.0  # Convert to seconds
        
        print(f"Audio duration: {total_duration:.2f} seconds")
        
        # Load and resize the image
        img = Image.open(image_path)
        w, h = img.size
        
        # Use portrait orientation for better mobile viewing
        target_width = 1080
        target_height = 1920
        
        # Create the background image clip
        image_clip = (mp.ImageClip(str(image_path))
                      .set_duration(total_duration))
        
        # Resize while maintaining aspect ratio
        if w/h > target_width/target_height:  # Image is wider than target
            image_clip = image_clip.resize(height=target_height)
        else:  # Image is taller than target
            image_clip = image_clip.resize(width=target_width)
        
        # Center the image
        image_clip = image_clip.set_position(('center', 'center'))
        
        # Create black background
        bg_clip = mp.ColorClip(size=(target_width, target_height), color=(0, 0, 0))
        bg_clip = bg_clip.set_duration(total_duration)
        
        # List to hold all clips
        clips = [bg_clip, image_clip]
            
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
        
        # Create output video path
        video_files = list(output_dir.glob("video_*.mp4"))
        next_number = len(video_files) + 1 if video_files else 1
        output_path = output_dir / f"video_{next_number}.mp4"
        
        print("\n" + "="*50)
        print("STEP 2: CREATING VIDEO")
        print("="*50)
        video_path = create_video(image_file, speech_file, output_path)
        
        if not video_path:
            print("Failed to create video. Exiting.")
            sys.exit(1)
        
        print("\n" + "="*50)
        print("VIDEO CREATION COMPLETE!")
        print("="*50)
        print(f"Video saved to: {video_path}")
        print("="*50 + "\n")
        
        # Ensure console output is fully displayed before exiting
        sys.stdout.flush()
        time.sleep(1)
        
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        traceback.print_exc()
        sys.exit(1) 