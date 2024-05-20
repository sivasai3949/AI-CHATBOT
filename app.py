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
        "model": "gpt-3.5-turbo",
        "messages": conversation_history + [
            {"role": "user", "content": input_text}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error: Failed to get response from OpenAI API"

def main():
    st.title("RoboTutor - Educational Chatbot")
    st.write("Hi there! How can I assist you today?")

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]

    user_input = st.text_input("Type your message...")

    api_key = st.secrets["OPENAI_API_KEY"]  # Retrieve API key from Streamlit Secrets

    if st.button("Send"):
        if user_input:
            st.session_state.conversation_history.append({"role": "user", "content": user_input})
            response = get_ai_response(user_input, api_key, st.session_state.conversation_history)
            st.session_state.conversation_history.append({"role": "assistant", "content": response})

            st.write("You:", user_input)
            st.write("Bot:", response)

    if st.button("Clear Conversation"):
        st.session_state.conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]
        st.write("Conversation cleared!")

    # Display the conversation history
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            st.write("You:", message["content"])
        elif message["role"] == "assistant":
            st.write("Bot:", message["content"])

if __name__ == "__main__":
    main()
