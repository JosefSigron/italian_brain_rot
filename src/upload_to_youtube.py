import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
from pathlib import Path


def get_latest_file_number(directory, prefix, extension):
    """Find the highest numbered file with the given prefix and extension."""
    files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(extension)]
    if not files:
        return 0
    numbers = [int(f.split('_')[1].split('.')[0]) for f in files]
    return max(numbers)


def get_latest_video_path():
    """Get the path to the latest generated video file."""
    # Path to the videos directory (relative to this script)
    videos_dir = Path(__file__).parent / "../results/videos"
    
    # Get the latest video number
    video_num = get_latest_file_number(videos_dir, "video", "mp4")
    
    # Get the path to the latest video
    video_path = videos_dir / f"video_{video_num}.mp4"
    
    if not video_path.exists():
        raise FileNotFoundError(f"Latest video file not found: {video_path}")
    
    return video_path


def get_first_line_transcript():
    """Get the content of the latest transcript file for video description."""
    transcripts_dir = Path(__file__).parent / "../results/transcripts"
    
    transcript_path = transcripts_dir / "first_line_transcript.txt"
    
    if not transcript_path.exists():
        return "AI-generated cat story video"
    
    with open(transcript_path, "r") as f:
        content = f.read().strip()
    
    # Transform "A x Story." into "A x cat Story"
    if "sad" in content.lower():
        content = content.replace("sad", "sad cat")
    elif "sexy" in content.lower():
        content = content.replace("sexy", "sexy cat")
    elif "scary" in content.lower():
        content = content.replace("scary", "scary cat")

    print(f"Video Title: {content}")

    return content


def get_authenticated_service():
    """Get an authenticated YouTube API service."""
    print("\nAuthenticating with YouTube API...")
    # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
    # the OAuth 2.0 information for this application, including its client_id and
    # client_secret. You can acquire an OAuth 2.0 client ID and client secret from
    # the Google Cloud Console at https://cloud.google.com/console.
    CLIENT_SECRETS_FILE = "client_secret.json"
    
    # This OAuth 2.0 access scope allows an application to upload files to the
    # authenticated user's YouTube channel, but doesn't allow other types of access.
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    
    # Flow to handle OAuth authorization
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    print("\nOpening browser for authentication. Please follow the prompts...")
    credentials = flow.run_local_server(port=8080)
    
    print("Authentication successful!")
    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)


def upload_video(video_path):
    """Upload the video to YouTube."""
    try:
        # Get authenticated service
        youtube = get_authenticated_service()
        
        # Get latest transcript for video description
        description = get_first_line_transcript()
        print(f"\nVideo type: {description}")
        
        # Define video metadata
        body = {
            "snippet": {
                "title": f"{description} #shorts",
                "description": f"{description} #Shorts, #AI, #ComfyUI, #GPT-4o",
                "tags": ["AI", "Cat Story", "Generated Video", "ComfyUI", "GPT-4o", "Shorts"]
            },
            "status": {
                "privacyStatus": "public"  # Changed from "private" to "public"
            }
        }
        
        print(f"\nPreparing to upload: {Path(video_path).name}")
        print(f"Title: {body['snippet']['title']}")
        print(f"Privacy: {body['status']['privacyStatus']}")
        
        # Create upload request
        insert_request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=googleapiclient.http.MediaFileUpload(
                video_path, 
                resumable=True
            )
        )
        
        # Execute upload with progress tracking
        response = None
        print(f"\nUploading file: {video_path}...")
        print("Progress: ", end="")
        
        while response is None:
            status, response = insert_request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"{progress}%... ", end="", flush=True)
        
        print("100% Complete!")
        
        video_id = response["id"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"\nVideo uploaded successfully!")
        print(f"Video ID: {video_id}")
        print(f"Video URL: {video_url}")
        
        return video_url
    
    except Exception as e:
        print(f"\nAn error occurred during upload: {e}")
        return None


def main():
    print("\n" + "="*50)
    print("          YOUTUBE VIDEO UPLOADER")
    print("="*50)
    
    try:
        # Get the latest video path
        print("\nLooking for the latest generated video...")
        video_path = get_latest_video_path()
        print(f"Found video: {video_path}")
        
        # Upload the video
        print("\n" + "="*50)
        print("          UPLOADING TO YOUTUBE")
        print("="*50)
        upload_url = upload_video(video_path)
        
        print("\n" + "="*50)
        if upload_url:
            print("          UPLOAD SUCCESSFUL!")
            print("="*50)
            print(f"Your video is now available at:")
            print(f"{upload_url}")
        else:
            print("          UPLOAD FAILED")
            print("="*50)
            print("Please check the error messages above.")
        print("="*50 + "\n")
    
    except FileNotFoundError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main() 