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
    st.write("This is the Transcript content.")
elif st.session_state.active_button == "Note":
    st.write("This is the Note content.")
