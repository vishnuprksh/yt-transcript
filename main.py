import streamlit as st

# Embed YouTube video
video_url = "https://www.youtube.com/watch?v=ARMk955pGbg"
st.markdown(f"""
    <iframe width="560" height="315" src="{video_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
""", unsafe_allow_html=True)

# Clickable timestamps
timestamps = {
    "Introduction": "0m10s",
    "Topic 1": "1m30s",
    "Topic 2": "3m45s",
    "Topic 3": "5m20s",
    "Conclusion": "7m00s"
}

st.write("### Jump to specific sections:")
for title, time in timestamps.items():
    st.write(f"[{title}](https://youtu.be/YOUR_VIDEO_ID?t={time})")
