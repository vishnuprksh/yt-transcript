import streamlit as st
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import streamlit.components.v1 as components
from datetime import datetime

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Function to get YouTube video ID from a URL
def get_video_id(url: str) -> str:
    """Extracts the video ID from a YouTube URL."""
    if "watch?v=" in url:
        return url.split("watch?v=")[-1]
    return url.split("/")[-1]

# Function to format transcript using GPT-4o-mini API
def format_transcript(text: str, source_url: str) -> str:
    """Formats the transcript text using the GPT-4o-mini API."""
    # Add metadata header with source URL and timestamp
    metadata = f"""Source: {source_url}
Retrieved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"""
    
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
    
    # Combine metadata with formatted transcript
    return metadata + completion.choices[0].message.content.strip()

# Function to fetch transcript from YouTube
def fetch_transcript(video_id: str) -> str:
    """Fetches the raw transcript from a YouTube video."""
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return ". ".join(entry['text'] for entry in transcript) + "."

# Streamlit app title
st.title("YouTube Video Transcript Viewer")

# Input field for YouTube URL
youtube_url = st.text_input("Enter YouTube Video URL:", "")

if youtube_url:
    video_id = get_video_id(youtube_url)
    full_url = f"https://www.youtube.com/watch?v={video_id}"

    # Display embedded YouTube video
    st.video(full_url)

    # Check if the formatted transcript exists in session state
    if "formatted_transcript" not in st.session_state or st.session_state.get("current_video_id") != video_id:
        # Fetch and format transcript only once
        raw_text = fetch_transcript(video_id)
        formatted_transcript = format_transcript(raw_text, full_url)
        st.session_state["formatted_transcript"] = formatted_transcript
        st.session_state["current_video_id"] = video_id
    else:
        formatted_transcript = st.session_state["formatted_transcript"]

    # Display the formatted transcript under an <article> tag
    st.markdown(f"<article style='white-space: pre-wrap;'>{formatted_transcript}</article>", 
               unsafe_allow_html=True)

    # JavaScript for "Copy to Clipboard"
    copy_script = f"""
    <script>
    function copyToClipboard() {{
        const textToCopy = `{formatted_transcript.replace("`", "\\`")}`;
        navigator.clipboard.writeText(textToCopy).then(function() {{
            alert('Transcript copied to clipboard!');
        }}, function(err) {{
            console.error('Could not copy text: ', err);
        }});
    }}
    </script>
    <button onclick="copyToClipboard()">Copy Transcript</button>
    """
    
    # Embed the script and button using Streamlit components
    components.html(copy_script, height=40)