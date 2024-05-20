import streamlit as st
import requests
import json

def get_ai_response(input_text, api_key, conversation_history):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",  # Updated model
        "messages": conversation_history + [
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

    conversation_history = []

    while True:
        user_input = st.text_input("You:")

        api_key = st.secrets["OPENAI_API_KEY"]  # Retrieve API key from Streamlit Secrets

        if st.button("Send"):
            if user_input:
                conversation_history.append({"role": "user", "content": user_input})
                response = get_ai_response(user_input, api_key, conversation_history)
                conversation_history.append({"role": "bot", "content": response})
                st.write("Bot:", response)
            else:
                st.write("Please type something.")

        if st.button("Clear Conversation"):
            conversation_history = []

        if st.button("End Conversation"):
            break

if __name__ == "__main__":
    main()
