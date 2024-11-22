import streamlit as st
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

# st.set_page_config(layout="wide")

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
                "content": f"""Add suitable headings and subheadings to the following transcript without any modifications to the transcript : \n\n{text}"""
            }
        ]
    )
    return completion.choices[0].message.content.strip()

# Function to fetch, format, and display the transcript
def display_transcript(video_id: str):
    """Fetches the transcript, formats it using GPT-4o-mini API, and displays it under an <article> tag."""
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    raw_text = ". ".join(entry['text'] for entry in transcript) + "."
    
    # Format the raw transcript using GPT-4o-mini
    formatted_text = format_transcript(raw_text)
    
    # Display the formatted transcript under an <article> tag
    st.markdown(f"<article style='white-space: pre-wrap;'>{formatted_text}</article>", unsafe_allow_html=True)

# Streamlit app title
st.title("YouTube Video Transcript Viewer")

# Input field for YouTube URL
youtube_url = st.text_input("Enter YouTube Video URL:", "")

if youtube_url:
    video_id = get_video_id(youtube_url)

    # Display embedded YouTube video
    st.video(f"https://www.youtube.com/watch?v={video_id}")

    # Fetch, format, and display the transcript
    display_transcript(video_id)
