from pathlib import Path
from openai import OpenAI
import sys
import time
import traceback
import random

def generate_response():
    print("Generating story from GPT-4o...")
    try:
        client = OpenAI()
        
        # Define some potential fruits and animals for the prompts
        fruits = ["apple", "banana", "grape", "pineapple", "strawberry", "watermelon", "kiwi", "mango", "peach"]
        animals = ["cat", "dog", "elephant", "lion", "tiger", "monkey", "bear", "wolf", "fox", "rabbit"]
        
        # Randomly select one fruit and one animal
        chosen_fruit = random.choice(fruits)
        chosen_animal = random.choice(animals)
        
        # Create the prompt for GPT-4o
        prompt = f"""I'll give you two words: {chosen_fruit} and {chosen_animal}.

Follow these instructions exactly:
1. First row: Show only these 2 words.
2. Second row: Translate these 2 words into Italian (2 words only).
3. Write a short story in Italian about this hybrid creature (4-5 sentences).
4. Each sentence should be on its own line with a blank line after it.
5. Keep sentences simple (8 words maximum per sentence).
"""
        
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a creative storyteller who writes in Italian."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        response_text = completion.choices[0].message.content.strip()
        
        # Ensure proper formatting with blank lines between sentences
        lines = response_text.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.strip():  # If the line is not empty
                formatted_lines.append(line)
                formatted_lines.append("")  # Add a blank line after each non-empty line
        
        formatted_response = '\n'.join(formatted_lines).strip()
        
        print("\nGenerated text:")
        print(formatted_response[:200] + "...\n")
        
        return formatted_response
    except Exception as e:
        print(f"Error generating story: {e}")
        traceback.print_exc()
        return None

def save_text(text, output_dir="../results/transcripts"):
    print("Saving transcript files...")
    try:
        # Create the transcripts directory if it doesn't exist
        output_dir_path = Path(__file__).parent / output_dir
        output_dir_path.mkdir(parents=True, exist_ok=True)

        # Find the next available file name
        existing_files = list(output_dir_path.glob("transcript_*.txt"))
        next_number = len(existing_files) + 1 if existing_files else 1

        # Create the new transcript file path
        transcript_file_path = output_dir_path / f"transcript_{next_number}.txt"

        # Save the complete text to the transcript file
        with open(transcript_file_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        # Extract and save the first line to a separate file
        lines = text.split('\n')
        first_line = lines[0] if lines else ""
        
        first_line_path = output_dir_path / "first_line_transcript.txt"
        with open(first_line_path, "w", encoding="utf-8") as f:
            f.write(first_line)
        
        return transcript_file_path
    except Exception as e:
        print(f"Error saving transcript: {e}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    try:
        print("\n" + "="*50)
        print("STEP 1: GENERATING STORY TEXT")
        print("="*50)
        response_text = generate_response()
        
        if response_text is None:
            print("Failed to generate story text. Exiting.")
            sys.exit(1)
        
        print("\n" + "="*50)
        print("STEP 2: SAVING TRANSCRIPTS")
        print("="*50)
        transcript_file = save_text(response_text)
        
        if transcript_file is None:
            print("Failed to save transcript. Exiting.")
            sys.exit(1)
        
        print("\n" + "="*50)
        print("TEXT GENERATION COMPLETE!")
        print("="*50)
        print(f"Transcript saved to: {transcript_file}")
        print(f"First line saved to: first_line_transcript.txt")
        print("="*50 + "\n")
        
        # Ensure console output is fully displayed before exiting
        sys.stdout.flush()
        time.sleep(1)
        
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        traceback.print_exc()
        sys.exit(1) 