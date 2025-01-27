import streamlit as st

# Initialize session state for active button
if "active_button" not in st.session_state:
    st.session_state.active_button = "Transcript"  # Default button

# Create columns for horizontal button layout
col1, col2 = st.columns(2)

# Buttons in columns
with col1:
    if st.button("Transcript"):
        st.session_state.active_button = "Transcript"

with col2:
    if st.button("Note"):
        st.session_state.active_button = "Note"

# Display text based on the active button
if st.session_state.active_button == "Transcript":
    st.write("### Transcript Content")
    st.write("""
        Welcome to the Transcript section! Here, you can review detailed 
        discussions, summaries, and insights. Below is a sample content:
        
        - **Introduction:** A brief overview of the topic, highlighting key objectives and purpose.
        - **Main Body:** In-depth analysis of the subject matter, including data points, findings, and supporting details.
        - **Conclusion:** A wrap-up summarizing the key takeaways and action points.
        
        Example Transcript:
        ```
        Speaker 1: Can you elaborate on the project's primary goals?
        Speaker 2: Certainly! The project aims to improve accessibility and enhance user engagement.
        Speaker 1: That’s insightful. Let’s delve deeper into the challenges faced during implementation.
        ```
    """)

elif st.session_state.active_button == "Note":
    st.write("### Notes Section")
    st.write("""
        Welcome to the Notes section! This is where you can keep track of 
        important points, annotations, and quick thoughts. Here’s a sample layout:
        
        - **Key Points:** Highlighted ideas or findings.
        - **Questions:** Any unresolved queries or areas for further exploration.
        - **Next Steps:** Action items or tasks to follow up on.
        
        Example Notes:
        - Point 1: Focus on improving data accuracy by implementing robust validation.
        - Point 2: Schedule a follow-up meeting with the development team.
        - Question: How can we enhance the user onboarding process?
        - Next Step: Draft a detailed proposal for the UI redesign.
    """)
