import re
import streamlit as st
from openai import OpenAI
from groq import Groq
from youtube_transcript_api import YouTubeTranscriptApi
import streamlit.components.v1 as components
from datetime import datetime

# Initialize clients
openai_client = OpenAI(api_key=st.secrets["openai"]["api_key"])
groq_client = Groq(api_key=st.secrets["groq"]["api_key"])

# Function to get YouTube video ID from a URL
def get_video_id(url: str) -> str:
    """Extracts the video ID from a YouTube URL."""
    if "watch?v=" in url:
        return url.split("watch?v=")[-1]
    return url.split("/")[-1]

# Function to call GPT-4o-mini via OpenAI
def call_gpt_model(prompt: str) -> str:
    """Calls GPT-4o-mini model and returns the result."""
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content.strip()

# Function to call Groq's R1 model
def call_groq_model(prompt: str) -> str:
    """Calls Groq's R1 model and returns the result, removing <think>...</think> sections."""
    completion = groq_client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_completion_tokens=1024,
        top_p=0.95,
        stream=False
    )
    full_output = completion.choices[0].message.content
    # Remove <think>...</think> tags from the output
    return re.sub(r"<think>.*?</think>", "", full_output, flags=re.DOTALL).strip()

# Function to format transcript using the selected model
def format_transcript(text: str, source_url: str, model: str) -> str:
    """Formats the transcript text using the selected model."""
    prompt = f"""You are a helpful assistant tasked with adding headings to a YouTube transcript, 
    preserving all content without removal or summarization. 
    Additionally, you should correct any grammatical errors in the text while keeping the original meaning intact. 
    The text should remain exactly as it is, except for necessary grammar fixes. 
    Your task is to add headings before sections of the transcript to indicate topic changes, speaker changes, 
    or logical breaks in the flow, but the content should not be shortened, summarized, or altered in any other way.

    Transcript:
    {text}"""

    if model == "GPT-4o-mini":
        return call_gpt_model(prompt)
    elif model == "Groq R1":
        return call_groq_model(prompt)

# Function to generate study notes using the selected model
def generate_study_note(transcript: str, source_url: str, model: str) -> str:
    """Generates a detailed study note from the transcript using the selected model."""
    prompt = f"""
transcript
\"\"\"{transcript}\"\"\"

PURPOSE:
- Change the following transcript into a detailed study note (talking style to layman style explanation). 
IMPORTANT:
- Mention the source of the video (Source: {source_url})
- Strictly do not lose data during conversion even if it seems irrelevant (calculations, examples...etc).
- If equations are mentioned, render using latex
- STRICTLY do not enclose latex equations in brackets (enclose in single or double dollar signs instead)
- If images are used in the explanation, use a name (eg: fig1, fig2...etc.) and explain the topic in the note. Strictly do not miss the data.
- For the mentioned images, provide placeholders in the note(name and a brief explantion).
- The placeholders should be properly placed during the note, do not keep it for end of the note.
"""
    if model == "GPT-4o-mini":
        return call_gpt_model(prompt)
    elif model == "Groq R1":
        return call_groq_model(prompt)

# Function to fetch transcript from YouTube
def fetch_transcript(video_id: str) -> str:
    """Fetches the raw transcript from a YouTube video."""
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return ". ".join(entry['text'] for entry in transcript) + "."

# Streamlit app title
st.title("YouTube Video Transcript Viewer")

# Input field for YouTube URL
youtube_url = st.text_input("Enter YouTube Video URL:", "")

# Dropdown to select the model
model_option = st.selectbox("Choose a model:", ["GPT-4o-mini", "Groq R1"])

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
        # Fetch and format the transcript using the selected model
        raw_text = fetch_transcript(video_id)
        formatted_transcript = format_transcript(raw_text, full_url, model_option)

        # Display the formatted transcript
        st.markdown(f"<article style='white-space: pre-wrap;'>{formatted_transcript}</article>", 
                    unsafe_allow_html=True)

        # Add a copy button for the transcript
        copy_script_transcript = f"""
        <script>
        function copyTranscript() {{
            const textToCopy = `{formatted_transcript.replace("`", "\\`")}`;
            navigator.clipboard.writeText(textToCopy).then(function() {{
                alert('Transcript copied to clipboard!');
            }}, function(err) {{
                console.error('Could not copy text: ', err);
            }});
        }}
        </script>
        <button onclick="copyTranscript()">Copy Transcript</button>
        """
        components.html(copy_script_transcript, height=40)

    elif note_button:
        # Generate the study note using the selected model
        raw_text = fetch_transcript(video_id)
        study_note = generate_study_note(raw_text, full_url, model_option)

        # Display the generated study note
        st.markdown(f"<article style='white-space: pre-wrap;'>{study_note}</article>", 
                    unsafe_allow_html=True)

        # Add a copy button for the study note
        copy_script_note = f"""
        <script>
        function copyNote() {{
            const textToCopy = `{study_note.replace("`", "\\`")}`;
            navigator.clipboard.writeText(textToCopy).then(function() {{
                alert('Study Note copied to clipboard!');
            }}, function(err) {{
                console.error('Could not copy text: ', err);
            }});
        }}
        </script>
        <button onclick="copyNote()">Copy Study Note</button>
        """
        components.html(copy_script_note, height=40)
