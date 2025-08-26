from pathlib import Path
import requests
import json
import sys
import time
import traceback
import os

def read_transcript(output_dir="../results/transcripts"):
    print("Reading transcript file...")
    try:
        # Find the latest transcript file
        output_dir_path = Path(__file__).parent / output_dir
        transcript_files = list(output_dir_path.glob("transcript_*.txt"))
        
        if not transcript_files:
            print("No transcript files found.")
            return None
            
        latest_transcript = max(transcript_files, key=lambda x: int(x.stem.split('_')[1]))
        print(f"Found latest transcript: {latest_transcript}")
        
        # Read the transcript file
        with open(latest_transcript, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        
        # Skip the first two lines (hybrid name and Italian translation)
        # And get the rest of the content (the Italian story)
        italian_story_lines = []
        skip_lines = 1
        line_count = 0
        
        for line in lines:
            if line_count >= skip_lines:
                # Only add non-empty lines to avoid TTS pauses
                if line.strip():
                    italian_story_lines.append(line.strip())
            if line.strip(): # Only count non-empty lines
                line_count += 1
        
        # Join sentences with spaces instead of newlines to avoid TTS pauses
        italian_story = ' '.join(italian_story_lines)
        print(f"Extracted Italian story text ({len(italian_story_lines)} lines)")
        
        return italian_story
    except Exception as e:
        print(f"Error reading transcript: {e}")
        traceback.print_exc()
        return None

def text_to_speech(text, output_dir="../results/speeches", voice_id="pNInz6obpgDQGcFmaJgB"):
    print("Converting text to speech using ElevenLabs...")
    try:
        # Get ElevenLabs API key from environment variable
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            print("Error: ELEVENLABS_API_KEY environment variable not set.")
            print("Please set your ElevenLabs API key:")
            print("On Windows: set ELEVENLABS_API_KEY=your_api_key_here")
            print("On Unix/Mac: export ELEVENLABS_API_KEY=your_api_key_here")
            return None
        
        output_dir_path = Path(__file__).parent / output_dir
        output_dir_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

        # Find the next available file name
        existing_files = list(output_dir_path.glob("speech_*.mp3"))
        next_number = len(existing_files) + 1 if existing_files else 1
        speech_file_path = output_dir_path / f"speech_{next_number}.mp3"

        # ElevenLabs API endpoint
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        # Headers for the API request
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        # Request payload
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",  # Use multilingual model for Italian
            "voice_settings": {
                "speed": 1.2,  # Slightly faster speech
                "stability": 0.5,  # Lower stability for more dynamic/excited speech
                "similarity_boost": 0.8,  # Slightly higher to maintain voice character
                "style": 0.9,  # High style for excited/emotional delivery
                "use_speaker_boost": True
            }
        }
        
        print("Sending request to ElevenLabs API...")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            # Save the audio file
            with open(speech_file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Speech file saved to: {speech_file_path}")
            return speech_file_path
        else:
            print(f"Error from ElevenLabs API: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error converting text to speech: {e}")
        traceback.print_exc()
        return None

def list_available_voices():
    """List available voices from ElevenLabs"""
    try:
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            print("Error: ELEVENLABS_API_KEY environment variable not set.")
            return
        
        url = "https://api.elevenlabs.io/v1/voices"
        headers = {
            "xi-api-key": api_key
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            voices = response.json()
            print("\nAvailable voices:")
            print("=" * 50)
            for voice in voices["voices"]:
                print(f"ID: {voice['voice_id']}")
                print(f"Name: {voice['name']}")
                print(f"Category: {voice.get('category', 'N/A')}")
                print(f"Description: {voice.get('description', 'N/A')}")
                print("-" * 30)
        else:
            print(f"Error fetching voices: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error listing voices: {e}")

if __name__ == "__main__":
    try:
        print("\n" + "="*50)
        print("STEP 1: READING TRANSCRIPT")
        print("="*50)
        italian_text = read_transcript()
        
        if italian_text is None:
            print("Failed to read transcript. Exiting.")
            sys.exit(1)
        
        print("\n" + "="*50)
        print("STEP 2: CONVERTING TO SPEECH")
        print("="*50)
        speech_file = text_to_speech(italian_text)
        
        if speech_file is None:
            print("Failed to convert text to speech. Exiting.")
            sys.exit(1)
        
        print("\n" + "="*50)
        print("SPEECH GENERATION COMPLETE!")
        print("="*50)
        print(f"Speech saved to: {speech_file}")
        print("="*50 + "\n")
        
        # Ensure console output is fully displayed before exiting
        sys.stdout.flush()
        time.sleep(1)
        
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        traceback.print_exc()
        sys.exit(1) 