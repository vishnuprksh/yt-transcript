import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(youtube_url: str) -> str:
    """
    Extracts the video ID from a YouTube URL.

    Args:
        youtube_url (str): The full YouTube URL.

    Returns:
        str: The extracted video ID.
    """
    # Regular expression to match the video ID in the YouTube URL
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', youtube_url)
    
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def fetch_youtube_transcript(youtube_url: str) -> str:
    """
    Fetches the transcript of a YouTube video using its URL.

    Args:
        youtube_url (str): The full YouTube video URL.

    Returns:
        str: The concatenated transcript text without timestamps.
    """
    try:
        # Extract the video ID from the URL
        video_id = extract_video_id(youtube_url)
        
        # Fetch the transcript using the extracted video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Concatenate the transcript text, removing timestamps
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage:
youtube_url = 'https://www.youtube.com/watch?v=RBSUwFGa6Fk&t=3s&pp=ygUMZGF0YSBzY2llbmNl'
transcript_text = fetch_youtube_transcript(youtube_url)
print(transcript_text)