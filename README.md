# Italian Brain Rot Video Generator

This project generates quirky videos featuring a fruit-animal hybrid character with Italian narration. The system orchestrates a complete pipeline:

1. **Text Generation**: Creates a hybrid fruit-animal name and a story in Italian
2. **Image Generation**: Creates an image of the hybrid character
3. **Speech Generation**: Converts the Italian story to speech
4. **Video Creation**: Combines the image and the speech
5. **YouTube Upload**: Optionally uploads the video to YouTube

## Setup Instructions

### Prerequisites

- Python 3.8+
- OpenAI API key (for GPT-4o, DALL-E, and TTS)
- ffmpeg
- YouTube API credentials (for video upload)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/JosefSigron/italian_brain_rot
   ```

2. Install the required dependencies:
   ```
   pip install openai moviepy pydub vosk pillow tqdm requests google-api-python-client google-auth-oauthlib google-auth-httplib2
   ```

3. Set up your OpenAI API key:
   ```
   export OPENAI_API_KEY="your_api_key_here"
   ```
   (On Windows, use `set OPENAI_API_KEY=your_api_key_here`)
   
   For more information on how to set up your API visit: [OpenAI API](https://platform.openai.com/docs/libraries)

4. Set up YouTube API credentials (If you are not planning on uploading to youtube, you may skip this step):
   1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
   2. Create a new project or select an existing one
   3. Enable the YouTube Data API v3 for your project
   4. Go to "Credentials" and click "Create Credentials"
   5. Select "OAuth 2.0 Client ID"
   6. Choose "Desktop app" as the application type
   7. Download the client configuration file
   8. Rename it to `client_secret.json` and place it in the project root directory
   9. The first time you run the upload script, it will open a browser window for authentication

## Usage

### Run the Complete Pipeline

To run the entire process from text generation to video creation:

```
python src/run_all.py
```
OR
```
./run_italian_brain_rot.bat
```

### Run Individual Components

Each component can be run independently:

1. Generate text:
   ```
   python src/generate_text.py
   ```

2. Generate image:
   ```
   python src/generate_image.py
   ```

3. Generate speech:
   ```
   python src/generate_speech.py
   ```

4. Create video:
   ```
   python src/create_video.py
   ```

5. Upload to YouTube:
   ```
   python src/upload_to_youtube.py
   ```

## Output Files

All generated files are stored in the `results` directory:

- `results/transcripts/`: Story text and first line for the character name
- `results/images/`: Character images generated by DALL-E
- `results/speeches/`: Audio narration of the story
- `results/videos/`: Final videos

## Video Effects

The project includes the ability to add special effects to your videos:

### How to Add Video Effects

1. Download video effect overlays with transparent backgrounds/alpha channels from sources like:
   - [Videezy](https://www.videezy.com/free-video/fire-overlay) - Search for effects with "alpha channel"
   - [Pixabay](https://pixabay.com/videos/)
   - [Pexels](https://www.pexels.com/search/videos/)

2. Place the video effect files in the `assets/effects` directory. The script will automatically detect and use all effect files.
   - Supported formats: .mp4, .mov, .avi, .webm
   - For best results, use videos with alpha channels for proper transparency

### Effect Stacking

- Multiple effects will be layered on top of each other in alphabetical order by filename
- Each effect has a default opacity value of 0.2
- To control the order of effects, you can prefix filenames with numbers (e.g., "01_fire.mp4", "02_smoke.mp4")

### Built-in Animation Effects

The script also includes built-in animation effects that are applied directly to your image:

#### Grow and Turn Effect

- Similar to PowerPoint's "Grow & Turn" animation
- The image starts at 50% of its size and rotates 360° while growing to full size
- The animation lasts for approximately 2 seconds at the beginning of the video
- This effect is applied by default and works alongside any overlay effects you add

### Recommended Effects

- [Fiery Orange Glowing Burning Ash Particles](https://www.videezy.com/abstract/52551-fiery-orange-glowing-burning-ash-particles) - Fire sparks with transparent alpha channel
- [Flames Overlay](https://www.videezy.com/abstract/45126-burning-flames-frame-loop) - Burning flames

### Usage Notes

- The script automatically adjusts opacity for each effect, starting at 0.4 and gradually reducing for subsequent effects
- Effects are scaled to cover the entire frame
- All effects will loop for the duration of your video

## How It Works

1. `generate_text.py`:
   - Randomly selects a fruit and animal
   - Uses GPT-4o to create a hybrid character name and Italian story
   - Saves the output to the transcripts directory

2. `generate_image.py`:
   - Reads the character name from the transcript
   - Uses DALL-E 3 to create an image of the character
   - Saves the image to the images directory

3. `generate_speech.py`:
   - Reads the Italian story from the transcript
   - Uses OpenAI's TTS to generate speech
   - Saves the audio to the speeches directory

4. `create_video.py`:
   - Reads the latest image and speech file
   - Creates a video with the image and the audio
   - Applies any video effects found in the assets/effects directory
   - Applies the grow & turn animation effect to the image

5. `upload_to_youtube.py`:
   - Uses the YouTube Data API to upload the latest video
   - Handles OAuth2 authentication
   - Sets video title, description, and privacy settings

## Troubleshooting

- **OpenAI API Issues**: Ensure your API key is set correctly and you have sufficient credits.
- **Video Generation Issues**: Check that moviepy and its dependencies (like ffmpeg) are correctly installed.
- **YouTube Upload Issues**: 
  - Verify that `client_secret.json` is in the correct location
  - Check that you have enabled the YouTube Data API v3
  - Ensure you have completed the OAuth2 authentication process


## Acknowledgments

- [OpenAI](https://openai.com/) for GPT-4o, DALL-E 3, and TTS
- [MoviePy](https://zulko.github.io/moviepy/) for video generation
- [Google YouTube Data API](https://developers.google.com/youtube/v3) for video upload functionality 