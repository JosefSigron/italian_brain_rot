from pathlib import Path
from openai import OpenAI
import sys
import time
import traceback
import base64

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
    print(f"Generating image from gpt-image-1 for: {text}...")
    try:
        client = OpenAI()
        
        # Split the hybrid name into its components
        # Assuming format like "Airplane Cat" (where Airplane is object, Cat is animal)
        words = text.split()
        if len(words) >= 2:
            object_name = words[0]
            animal = words[1]
        else:
            # Fallback if we don't have proper word split
            object_name = text
            animal = text
        
        # Create an enhanced prompt for DALL-E using the requested format
        prompt = f"""Create an image of a {object_name} with a {animal} head.
        The image would look unrealistic.
        The background should be of a beautiful landscape.
"""
        
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1536",
            quality="high"
        )
        
        image_base64 = result.data[0].b64_json
        print("Image generated successfully with base64 encoding.")
        
        return image_base64
    except Exception as e:
        print(f"Error generating image: {e}")
        traceback.print_exc()
        return None

def save_image(image_base64, output_dir="../results/images"):
    print("Saving image...")
    try:
        # Create the images directory if it doesn't exist
        output_dir_path = Path(__file__).parent / output_dir
        output_dir_path.mkdir(parents=True, exist_ok=True)
        
        # Find the next available file name
        existing_files = list(output_dir_path.glob("image_*.png"))
        next_number = len(existing_files) + 1 if existing_files else 1
        
        # Create the new image file path
        image_file_path = output_dir_path / f"image_{next_number}.png"
        
        # Decode base64 and save the image
        image_bytes = base64.b64decode(image_base64)
        with open(image_file_path, "wb") as f:
            f.write(image_bytes)
                
        print(f"Image saved to: {image_file_path}")
        return image_file_path
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
        image_base64 = generate_image(first_line)
        
        if image_base64 is None:
            print("Failed to generate image. Exiting.")
            sys.exit(1)
        
        print("\n" + "="*50)
        print("STEP 3: SAVING IMAGE")
        print("="*50)
        image_file = save_image(image_base64)
        
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