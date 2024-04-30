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

if __name__ == "__main__":
    main()
