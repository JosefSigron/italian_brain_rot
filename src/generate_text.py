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
        
        # Define some potential objects and animals for the prompts
        objects = [
            # Technology & Electronics
            "airplane", "laptop", "robot", "camera", "smartphone", "tablet", "headphones", "microphone", "speaker", "printer", "keyboard", "mouse", "monitor", "drone", "satellite", "rocket", "submarine", "telescope", "microscope", "calculator", "watch", "clock", "radio", "television", "projector", "scanner", "router", "modem", "antenna", "battery", "charger",
            
            # Household Items
            "chair", "table", "bed", "sofa", "lamp", "mirror", "vase", "pillow", "blanket", "curtain", "carpet", "painting", "frame", "shelf", "cabinet", "drawer", "closet", "door", "window", "stairs", "elevator", "escalator", "fence", "gate", "mailbox", "garden", "fountain", "statue", "bench", "trashcan", "recycling bin",
            
            # Tools & Equipment
            "hammer", "screwdriver", "wrench", "pliers", "saw", "drill", "nail", "screw", "bolt", "nut", "tape", "glue", "rope", "chain", "lock", "key", "ladder", "scaffold", "crane", "bulldozer", "excavator", "tractor", "truck", "car", "motorcycle", "bicycle", "skateboard", "rollerblades", "skis", "snowboard", "surfboard",
            
            # Kitchen & Food Items
            "cup", "plate", "bowl", "fork", "spoon", "knife", "pot", "pan", "kettle", "toaster", "blender", "mixer", "oven", "refrigerator", "microwave", "dishwasher", "sink", "faucet", "stove", "grill", "barbecue", "cooler", "thermos", "lunchbox", "picnic basket", "wine glass", "beer bottle", "coffee maker", "tea pot", "salt shaker", "pepper mill",
            
            # Art & Creative Items
            "paintbrush", "paint", "canvas", "easel", "palette", "sculpture", "pottery", "jewelry", "necklace", "ring", "bracelet", "earrings", "crown", "tiara", "mask", "costume", "wig", "makeup", "perfume", "cologne", "soap", "shampoo", "toothbrush", "towel", "umbrella", "parasol", "flag", "banner", "balloon", "kite", "pinwheel",
            
            # Nature & Outdoor Items
            "cactus", "flower", "tree", "bush", "grass", "rock", "stone", "crystal", "gem", "diamond", "pearl", "shell", "coral", "mushroom", "leaf", "branch", "root", "seed", "sprout", "vine", "moss", "lichen", "algae", "seaweed", "sand", "soil", "clay", "mud", "snow", "ice", "rainbow",
            
            # Food & Fruits
            "apple", "banana", "grape", "pineapple", "strawberry", "watermelon", "kiwi", "mango", "peach", "orange", "blueberry", "raspberry", "blackberry", "cherry", "lemon", "lime", "coconut", "avocado", "tomato", "carrot", "potato", "onion", "garlic", "pepper", "cucumber", "lettuce", "spinach", "broccoli", "cauliflower", "corn", "peas",
            
            # Sports & Recreation
            "ball", "bat", "racket", "club", "stick", "puck", "disc", "frisbee", "hula hoop", "jump rope", "trampoline", "swing", "slide", "seesaw", "merry-go-round", "ferris wheel", "roller coaster", "bumper car", "arcade game", "puzzle", "board game", "card game", "dice", "spinner", "marble", "yo-yo", "kaleidoscope", "telescope", "binoculars", "compass", "map"
        ]
        
        animals = [
            # Domestic Animals
            "cat", "dog", "hamster", "guinea pig", "rabbit", "ferret", "bird", "parrot", "canary", "finch", "fish", "goldfish", "tropical fish", "turtle", "tortoise", "lizard", "snake", "gecko", "chameleon", "hermit crab", "mouse", "rat", "gerbil", "chinchilla", "hedgehog", "sugar glider", "pot-bellied pig", "miniature horse", "alpaca", "llama", "goat",
            
            # Farm Animals
            "cow", "horse", "pig", "sheep", "goat", "chicken", "duck", "turkey", "goose", "rooster", "donkey", "mule", "ox", "buffalo", "yak", "camel", "llama", "alpaca", "rabbit", "guinea pig", "hamster", "mouse", "rat", "gerbil", "chinchilla", "hedgehog", "sugar glider", "ferret", "skunk", "raccoon", "opossum",
            
            # Wild Mammals
            "elephant", "lion", "tiger", "leopard", "cheetah", "jaguar", "panther", "cougar", "lynx", "bobcat", "bear", "grizzly bear", "polar bear", "black bear", "panda bear", "koala", "kangaroo", "wallaby", "wombat", "platypus", "echidna", "monkey", "gorilla", "chimpanzee", "orangutan", "gibbon", "lemur", "sloth", "anteater", "armadillo", "pangolin",
            
            # Marine Animals
            "dolphin", "whale", "shark", "orca", "seal", "sea lion", "walrus", "otter", "beaver", "muskrat", "platypus", "duck-billed platypus", "sea turtle", "turtle", "tortoise", "crocodile", "alligator", "caiman", "gharial", "frog", "toad", "salamander", "newt", "axolotl", "fish", "goldfish", "tropical fish", "clownfish", "angelfish", "betta fish", "guppy",
            
            # Birds
            "eagle", "hawk", "falcon", "owl", "vulture", "condor", "albatross", "seagull", "penguin", "ostrich", "emu", "cassowary", "kiwi", "flamingo", "peacock", "pheasant", "quail", "partridge", "grouse", "turkey", "chicken", "duck", "goose", "swan", "heron", "egret", "stork", "crane", "ibis", "spoonbill", "pelican",
            
            # Insects & Arachnids
            "butterfly", "moth", "bee", "wasp", "hornet", "ant", "termite", "beetle", "ladybug", "firefly", "dragonfly", "damselfly", "grasshopper", "cricket", "cicada", "aphid", "spider", "scorpion", "centipede", "millipede", "caterpillar", "silkworm", "maggot", "larva", "pupa", "chrysalis", "cocoon", "web", "honeycomb", "anthill", "beehive",
            
            # Reptiles & Amphibians
            "snake", "python", "boa", "cobra", "viper", "rattlesnake", "copperhead", "cottonmouth", "coral snake", "sea snake", "lizard", "gecko", "chameleon", "iguana", "monitor lizard", "komodo dragon", "bearded dragon", "anole", "skink", "turtle", "tortoise", "sea turtle", "box turtle", "painted turtle", "snapping turtle", "frog", "toad", "tree frog", "poison dart frog", "bullfrog", "leopard frog",
            
            # Mythical & Fantasy
            "dragon", "unicorn", "phoenix", "griffin", "mermaid", "centaur", "minotaur", "pegasus", "hippogriff", "basilisk", "kraken", "leviathan", "sphinx", "chimera", "hydra", "cerberus", "cyclops", "troll", "ogre", "giant", "dwarf", "elf", "fairy", "pixie", "sprite", "nymph", "dryad", "naga", "yeti", "bigfoot", "loch ness monster"
        ]
        
        # Randomly select one object and one animal
        chosen_object = random.choice(objects)
        chosen_animal = random.choice(animals)
        
        # Create the prompt for GPT-4o
        prompt = f"""I'll give you two words: {chosen_object} and {chosen_animal}.

Follow these instructions exactly:
1. First row: Show only these 2 words
2. Second row: Create a funny and catchy name for the hybrid creature.
3. Third row: Write a short story in Italian about this hybrid creature (4-5 sentences).
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