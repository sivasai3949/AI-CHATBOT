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
    st.title("AI COUNSELLOR")
    st.write("Hi there! How can I assist you today?")

    # Initialize session state variables if they don't exist
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]
        st.session_state.chat_log = []

    # Initialize user input in session state if it doesn't exist
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # Layout for user input and buttons
    user_input = st.text_input("Type your message...", key="user_input")

    api_key = st.secrets["OPENAI_API_KEY"]  # Retrieve API key from Streamlit Secrets

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Send"):
            if st.session_state.user_input:
                st.session_state.conversation_history.append({"role": "user", "content": st.session_state.user_input})
                response = get_ai_response(st.session_state.user_input, api_key, st.session_state.conversation_history)
                st.session_state.conversation_history.append({"role": "assistant", "content": response})

                st.session_state.chat_log.append(("You", st.session_state.user_input))
                st.session_state.chat_log.append(("Counsellor", response))

                # Clear the user input after sending the message
                st.session_state.user_input = ""
                st.experimental_rerun()
    with col2:
        if st.button("Clear Input"):
            st.session_state.user_input = ""
            st.experimental_rerun()

    # Display the conversation history with a gap between responses
    st.write('<style>.message-gap { margin-top: 20px; }</style>', unsafe_allow_html=True)

    for sender, message in st.session_state.chat_log:
        if sender == "You":
            st.write(f"<div class='message-gap'>You: {message}</div>", unsafe_allow_html=True)
        elif sender == "Counsellor":
            st.write(f"<div class='message-gap'>Counsellor: {message}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
