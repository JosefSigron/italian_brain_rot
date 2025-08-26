#!/usr/bin/env python3
"""
ElevenLabs Setup and Test Script
This script helps you set up ElevenLabs TTS and test it with a sample text.
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Set up the ElevenLabs API key environment variable"""
    print("ElevenLabs TTS Setup")
    print("=" * 50)
    
    # Check if API key is already set
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if api_key:
        print(f"✅ ElevenLabs API key is already set: {api_key[:8]}...")
        return True
    
    print("To use ElevenLabs TTS, you need to:")
    print("1. Sign up at https://elevenlabs.io/")
    print("2. Get your API key from your profile")
    print("3. Set the environment variable")
    
    # Try to set the API key
    try:
        api_key = input("\nEnter your ElevenLabs API key: ").strip()
        if api_key:
            # Set environment variable for current session
            os.environ["ELEVENLABS_API_KEY"] = api_key
            
            # Try to save to a .env file for future use
            env_file = Path(__file__).parent.parent / ".env"
            try:
                with open(env_file, "w") as f:
                    f.write(f"ELEVENLABS_API_KEY={api_key}\n")
                print(f"✅ API key saved to {env_file}")
            except Exception as e:
                print(f"⚠️  Could not save to .env file: {e}")
                print("You'll need to set the environment variable manually each time.")
            
            print("✅ API key set successfully!")
            return True
        else:
            print("❌ No API key provided.")
            return False
    except KeyboardInterrupt:
        print("\n❌ Setup cancelled.")
        return False

def test_elevenlabs():
    """Test ElevenLabs TTS with a sample text"""
    print("\nTesting ElevenLabs TTS...")
    print("=" * 50)
    
    # Import the TTS function
    try:
        from generate_speech import text_to_speech, list_available_voices
    except ImportError as e:
        print(f"❌ Error importing TTS module: {e}")
        return False
    
    # Test with a sample Italian text
    sample_text = "Ciao! Questo è un test della sintesi vocale di ElevenLabs. La qualità dovrebbe essere molto migliore rispetto al modello precedente."
    
    print(f"Sample text: {sample_text}")
    print("\nGenerating speech...")
    
    # Generate speech
    speech_file = text_to_speech(sample_text)
    
    if speech_file:
        print(f"✅ Test successful! Speech file created: {speech_file}")
        print("You can now play this file to hear the quality difference.")
        return True
    else:
        print("❌ Test failed. Check the error messages above.")
        return False

def list_voices():
    """List available ElevenLabs voices"""
    print("\nListing available voices...")
    print("=" * 50)
    
    try:
        from generate_speech import list_available_voices
        list_available_voices()
    except ImportError as e:
        print(f"❌ Error importing TTS module: {e}")

def main():
    """Main setup function"""
    print("Italian Brain Rot - ElevenLabs TTS Setup")
    print("=" * 60)
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Setup incomplete. Please try again.")
        sys.exit(1)
    
    # List available voices
    list_voices()
    
    # Test TTS
    if test_elevenlabs():
        print("\n🎉 Setup complete! ElevenLabs TTS is working.")
        print("\nNext steps:")
        print("1. Run the main script: python src/run_all.py")
        print("2. Or test individual components: python src/generate_speech.py")
        print("\nNote: You may want to adjust the voice_id in generate_speech.py")
        print("to use a different voice from the list above.")
    else:
        print("\n❌ Setup failed. Please check the error messages and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
