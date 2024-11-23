import streamlit as st

def highlight_text(text: str, highlights: list) -> str:
    """
    Highlights specified portions of text by wrapping them in <mark> tags.

    Args:
        text (str): The main text content.
        highlights (list): List of phrases to highlight.

    Returns:
        str: Highlighted text as HTML.
    """
    for highlight in highlights:
        text = text.replace(highlight, f"<mark>{highlight}</mark>")
    return text

# UI Components
st.title("Text Highlighter")
text = st.text_area("Enter your text below:", height=200)

if text:
    st.write("### Original Text")
    st.write(text)

    # Highlighting Feature
    highlight_input = st.text_input("Enter text to highlight (comma-separated):")
    if highlight_input:
        highlights = [h.strip() for h in highlight_input.split(",")]
        highlighted_text = highlight_text(text, highlights)

        st.write("### Highlighted Text")
        st.markdown(highlighted_text, unsafe_allow_html=True)

        # Export Highlights
        if st.button("Export Highlights"):
            export_content = "\n".join(highlights)
            st.download_button(
                label="Download Highlights as Markdown",
                data=export_content,
                file_name="highlights.md",
                mime="text/markdown"
            )
