import streamlit as st
import requests
import json

def get_ai_response(input_text, api_key):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "text-davinci-003",  # Use the appropriate model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        # Handle error response
        return "Error: Failed to get response from OpenAI API"

def main():
    st.title("RoboTutor - Educational Chatbot")

    st.write("Hi there! How can I assist you today?")

    user_input = st.text_input("Type your message...")

    api_key = st.secrets["OPENAI_API_KEY"]  # Retrieve API key from Streamlit Secrets

    if st.button("Send"):
        if user_input:
            st.write("You:", user_input)
            response = get_ai_response(user_input, api_key)
            st.write("Bot:", response)

if __name__ == "__main__":
    main()
