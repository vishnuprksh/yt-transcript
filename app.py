import streamlit as st
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
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
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are a helpful assistant tasked with adding headings to a YouTube transcript, 
             preserving all content without removal or summarization. 
             Additionally, you should correct any grammatical errors in the text while keeping the original meaning intact. 
             The text should remain exactly as it is, except for necessary grammar fixes. 
             Your task is to add headings before sections of the transcript to indicate topic changes, speaker changes, 
             or logical breaks in the flow, but the content should not be shortened, summarized, or altered in any other way."""},

            {
                "role": "user",
                "content": f"""{text}"""
            }
        ]
    )
    
    formatted_text = completion.choices[0].message.content.strip()
    
    first_newline = formatted_text.find('\n')
    if first_newline == -1:
        return formatted_text  # If no newline found, return as is
    
    metadata = f"""Source: {source_url}
Retrieved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    
    final_text = (formatted_text[:first_newline + 1] + 
                 metadata + 
                 formatted_text[first_newline + 1:])
    
    return final_text

# Function to generate study notes using GPT
def generate_study_note(transcript: str, source_url: str) -> str:
    """Generates a detailed study note from the transcript using GPT."""
    prompt = f"""
transcript
\"\"\"{transcript}\"\"\"

PURPOSE:
- Change the following transcript into a detailed study note (talking style to layman style explanation). 
IMPORTANT:
- Mention the source of the video (Source: {source_url})
- Strictly do not lose data during conversion.
- Do not skip the data just because the image is not available. Use placeholders for images with names (fig1, fig2...etc.) to explain that part.
- Do not keep image placeholders to the end of the note. Place them properly during the note.
"""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant that creates detailed study notes from transcripts."},
                  {"role": "user", "content": prompt}]
    )
    
    return completion.choices[0].message.content.strip()

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

    # Add note above buttons
    st.markdown(
        """
        **Note**: Use the **Transcript** button to view the full transcript of the video.  
        Use the **Note** button to generate a concise, formatted, and easy-to-read study note.
        """
    )

    # Create columns for buttons
    col1, col2 = st.columns(2)

    # Buttons to toggle between transcript and note generation
    with col1:
        transcript_button = st.button("Transcript")
    with col2:
        note_button = st.button("Note")

    if transcript_button:
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

    elif note_button:
        # Check if study note already exists in session state
        if "study_note" not in st.session_state or st.session_state.get("current_video_id") != video_id:
            # Generate and store study note
            raw_text = fetch_transcript(video_id)
            study_note = generate_study_note(raw_text, full_url)
            st.session_state["study_note"] = study_note
            st.session_state["current_video_id"] = video_id
        else:
            study_note = st.session_state["study_note"]

        # Display the generated study note
        st.markdown(f"<article style='white-space: pre-wrap;'>{study_note}</article>", 
                    unsafe_allow_html=True)
