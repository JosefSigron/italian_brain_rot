import os
import sys
import time
import traceback
import subprocess
from pathlib import Path

def run_step(step_name, script_path):
    """Run a Python script and return success/failure"""
    print("\n" + "="*50)
    print(f"RUNNING STEP: {step_name}")
    print("="*50)
    
    try:
        # Get absolute path to the script
        script_abs_path = Path(__file__).parent / script_path
        
        # Run the script as a subprocess
        process = subprocess.Popen(
            [sys.executable, str(script_abs_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Stream the output in real-time
        for line in process.stdout:
            print(line.rstrip())
            
        # Wait for process to complete
        process.wait()
        
        # Check if process was successful
        if process.returncode == 0:
            print(f"\n✅ {step_name} completed successfully!")
            return True
        else:
            print(f"\n❌ {step_name} failed with exit code {process.returncode}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error running {step_name}: {e}")
        traceback.print_exc()
        return False

def ensure_directories_exist():
    """Create all necessary directories for the pipeline"""
    base_dir = Path(__file__).parent.parent
    dirs = [
        base_dir / "results",
        base_dir / "results/transcripts",
        base_dir / "results/images",
        base_dir / "results/speeches",
        base_dir / "results/videos",
    ]
    
    for directory in dirs:
        directory.mkdir(exist_ok=True, parents=True)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("ITALIAN BRAIN ROT VIDEO GENERATOR")
    print("="*50)
    
    # Ensure all directories exist
    ensure_directories_exist()
    
    # Define the steps to run in order
    steps = [
        ("Text Generation", "generate_text.py"),
        ("Image Generation", "generate_image.py"),
        ("Speech Generation", "generate_speech.py"),
        ("Video Creation", "create_video.py")
    ]
    
    # Run each step, stopping if one fails
    for step_name, script_path in steps:
        if not run_step(step_name, script_path):
            print("\n" + "="*50)
            print(f"Pipeline stopped due to failure in: {step_name}")
            print("="*50)
            sys.exit(1)
    
    print("\n" + "="*50)
    print("🎉 ALL STEPS COMPLETED SUCCESSFULLY! 🎉")
    print("="*50)
    print("\nYour Italian Brain Rot video has been created.")
    print("Check the 'results/videos' directory for the final video.")
    print("="*50) 