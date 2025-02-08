import streamlit as st
import requests
import os

API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

st.title("Music-AI")
st.write("Generate sample music by entering a prompt below:")

# Pre-existing sample prompts
sample_prompts = [
    "liquid drum and bass, atmospheric synths",
    "soothing bell sounds and starry night",
    "energetic pop using a guitar",
    "calm piano for relaxation",
    "upbeat jazz with saxophone"
]

# User input for music prompt
user_prompt = st.selectbox("Select a sample prompt:", sample_prompts)

# Option to enter a custom prompt
custom_prompt = st.text_input("Or enter your own music prompt:")

# Use custom prompt if provided, otherwise use selected sample prompt
final_prompt = custom_prompt if custom_prompt else user_prompt

# Store generated audio bytes in session state
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None

if st.button("Generate Music"):
    if final_prompt:
        st.session_state.audio_bytes = query({"inputs": f"{final_prompt}. Make sure to use the instrument mentioned properly"})  # Store audio bytes in session state

        # Remove existing output.mp3 if it exists
        output_file_path = "gen_music/output.mp3"
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

        # Save the audio as an MP3 file
        with open(output_file_path, "wb") as audio_file:
            audio_file.write(st.session_state.audio_bytes)

        # Display the audio
        st.audio(st.session_state.audio_bytes, format='audio/mp3')

        # Download button
        st.download_button(
            label="Download Music",
            data=st.session_state.audio_bytes,
            file_name="output.mp3",
            mime="audio/mp3"
        )
    else:
        st.warning("Please enter a prompt to generate music.")
