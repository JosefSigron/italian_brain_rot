from pathlib import Path
from openai import OpenAI
import sys
import time
import traceback

def read_first_line(file_path="../results/transcripts/first_line_transcript.txt"):
    print("Reading first line from transcript...")
    try:
        file_path = Path(__file__).parent / file_path
        
        if not file_path.exists():
            print(f"Error: File not found at {file_path}")
            return None
            
        with open(file_path, "r", encoding="utf-8") as f:
            first_line = f.read().strip()
            
        print(f"Retrieved first line: {first_line}")
        return first_line
    except Exception as e:
        print(f"Error reading first line: {e}")
        traceback.print_exc()
        return None

def generate_image(text):
    print(f"Generating image from DALL-E 3 for: {text}...")
    try:
        client = OpenAI()
        
        # Split the hybrid name into its components
        # Assuming format like "Apple Cat" (where Apple is fruit, Cat is animal)
        words = text.split()
        if len(words) >= 2:
            fruit = words[0]
            animal = words[1]
        else:
            # Fallback if we don't have proper word split
            fruit = text
            animal = text
        
        # Create an enhanced prompt for DALL-E using the requested format
        prompt = f"""Create an image of a {fruit} with a {animal} head.
"""
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        print(f"Image generated successfully. URL: {image_url}")
        
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        traceback.print_exc()
        return None

def save_image(image_url, output_dir="../results/images"):
    print("Saving image...")
    try:
        import requests
        
        # Create the images directory if it doesn't exist
        output_dir_path = Path(__file__).parent / output_dir
        output_dir_path.mkdir(parents=True, exist_ok=True)
        
        # Find the next available file name
        existing_files = list(output_dir_path.glob("image_*.png"))
        next_number = len(existing_files) + 1 if existing_files else 1
        
        # Create the new image file path
        image_file_path = output_dir_path / f"image_{next_number}.png"
        
        # Download and save the image
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_file_path, "wb") as f:
                f.write(response.content)
            
            # Also save as character_reference.png for potential use with ComfyUI
            character_ref_path = output_dir_path / "character_reference.png"
            with open(character_ref_path, "wb") as f:
                f.write(response.content)
                
            print(f"Image saved to: {image_file_path}")
            print(f"Character reference saved to: {character_ref_path}")
            return image_file_path
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error saving image: {e}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    try:
        print("\n" + "="*50)
        print("STEP 1: READING FIRST LINE FROM TRANSCRIPT")
        print("="*50)
        first_line = read_first_line()
        
        if first_line is None:
            print("Failed to read first line. Exiting.")
            sys.exit(1)
        
        print("\n" + "="*50)
        print("STEP 2: GENERATING IMAGE")
        print("="*50)
        image_url = generate_image(first_line)
        
        if image_url is None:
            print("Failed to generate image. Exiting.")
            sys.exit(1)
        
        print("\n" + "="*50)
        print("STEP 3: SAVING IMAGE")
        print("="*50)
        image_file = save_image(image_url)
        
        if image_file is None:
            print("Failed to save image. Exiting.")
            sys.exit(1)
        
        print("\n" + "="*50)
        print("IMAGE GENERATION COMPLETE!")
        print("="*50)
        print(f"Image saved to: {image_file}")
        print("="*50 + "\n")
        
        # Ensure console output is fully displayed before exiting
        sys.stdout.flush()
        time.sleep(1)
        
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        traceback.print_exc()
        sys.exit(1) 