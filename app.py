import streamlit as st
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Function to get YouTube video ID from a URL
def get_video_id(url: str) -> str:
    """Extracts the video ID from a YouTube URL."""
    if "watch?v=" in url:
        return url.split("watch?v=")[-1]
    return url.split("/")[-1]

# Function to format transcript using GPT-4o-mini API
def format_transcript(text: str) -> str:
    """Formats the transcript text using the GPT-4o-mini API."""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that formats transcripts."},
            {
                "role": "user",
                "content": f"Please format the following transcript text into a neat, readable format:\n\n{text}"
            }
        ]
    )
    return completion.choices[0].message.content.strip()

# Function to fetch, format, and display the transcript
def display_transcript(video_id: str):
    """Fetches the transcript, formats it using GPT-4o-mini API, and displays it."""
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    raw_text = ". ".join(entry['text'] for entry in transcript) + "."
    
    # Format the raw transcript using GPT-4o-mini
    formatted_text = format_transcript(raw_text)
    
    st.markdown(f"<div style='white-space: pre-wrap;'>{formatted_text}</div>", unsafe_allow_html=True)

# Streamlit app title
st.title("YouTube Video Transcript Viewer")

# Input field for YouTube URL
youtube_url = st.text_input("Enter YouTube Video URL:", "")

if youtube_url:
    video_id = get_video_id(youtube_url)

    # Display embedded YouTube video with increased size
    video_html = f"""
    <iframe width="100%" height="600px" src="https://www.youtube.com/embed/{video_id}" 
    frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen></iframe>
    """
    st.markdown(video_html, unsafe_allow_html=True)

    # Fetch, format, and display the transcript
    display_transcript(video_id)
