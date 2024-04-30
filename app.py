import streamlit as st
import openai
import io
from PIL import Image
import os

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_ai_response(input_text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text}
        ]
    )
    return completion.choices[0].message['content']

def main():
    st.title("RoboTutor - Educational Chatbot")

    st.write("Hi there! How can I assist you today?")

    user_input = st.text_input("Type your message...")

    if st.button("Send"):
        if user_input:
            st.write("You:", user_input)
            response = get_ai_response(user_input)
            st.write("Bot:", response)

    # Allow users to upload images
    image_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if image_file:
        st.write("Image uploaded successfully.")
        # Process the uploaded image
        # process_image(image_file.read())

    # Allow users to upload audio files
    audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav"])
    if audio_file:
        st.write("Audio uploaded successfully.")
        # Process the uploaded audio
        # process_audio(audio_file.read())

if __name__ == "__main__":
    main()
