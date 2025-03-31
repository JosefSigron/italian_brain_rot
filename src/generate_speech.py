from pathlib import Path
from openai import OpenAI
import sys
import time
import traceback

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
                italian_story_lines.append(line)
            if line.strip():  # Only count non-empty lines
                line_count += 1
        
        italian_story = '\n'.join(italian_story_lines)
        print(f"Extracted Italian story text ({len(italian_story_lines)} lines)")
        
        return italian_story
    except Exception as e:
        print(f"Error reading transcript: {e}")
        traceback.print_exc()
        return None

def text_to_speech(text, output_dir="../results/speeches", voice="ash"):
    print("Converting text to speech...")
    try:
        client = OpenAI()
        output_dir_path = Path(__file__).parent / output_dir
        output_dir_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

        # Find the next available file name
        existing_files = list(output_dir_path.glob("speech_*.mp3"))
        next_number = len(existing_files) + 1 if existing_files else 1
        speech_file_path = output_dir_path / f"speech_{next_number}.mp3"

        # Use Italian voice model if available, otherwise fallback to default
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
        )
        
        # Use the new method to stream the response content
        with open(speech_file_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Speech file saved to: {speech_file_path}")
        return speech_file_path
    except Exception as e:
        print(f"Error converting text to speech: {e}")
        traceback.print_exc()
        return None

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