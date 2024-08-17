import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str:
    """
    Extracts the YouTube video ID from a URL.

    Args:
        url (str): The full YouTube URL.

    Returns:
        str: The extracted video ID.
    """
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        if parsed_url.path[:7] == '/embed/':
            return parsed_url.path.split('/')[2]
        if parsed_url.path[:3] == '/v/':
            return parsed_url.path.split('/')[2]
    return None

def fetch_transcript(video_id: str):
    """
    Fetches the transcript for a given YouTube video ID.

    Args:
        video_id (str): The YouTube video ID.

    Returns:
        list: List of transcript items, each containing 'text' and 'start' keys.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

def display_transcript(transcript: list):
    """
    Displays the transcript on the Streamlit app.

    Args:
        transcript (list): The transcript to display.
    """
    st.subheader("Transcript")
    for entry in transcript:
        st.write(f"{entry['start']:.2f}s: {entry['text']}")

def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("YouTube Video with Transcript")

    url = st.text_input("Enter YouTube Video URL:")
    
    if url:
        video_id = extract_video_id(url)
        
        if video_id:
            # Embed the YouTube video
            st.video(f"https://www.youtube.com/embed/{video_id}")

            # Fetch and display the transcript
            transcript = fetch_transcript(video_id)
            
            if transcript:
                display_transcript(transcript)
        else:
            st.error("Invalid YouTube URL. Please enter a valid URL.")

if __name__ == "__main__":
    main()
