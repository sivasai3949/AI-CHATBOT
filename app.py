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

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]
        st.session_state.chat_log = []

    col1, col2 = st.columns([3, 1])

    with col1:
        user_input = st.text_input("Type your message...", key="user_input")

    with col2:
        if st.button("Clear Input"):
            st.session_state.user_input = ""  # Clear the user input

    api_key = st.secrets["OPENAI_API_KEY"]  # Retrieve API key from Streamlit Secrets

    if st.button("Send"):
        if user_input:
            st.session_state.conversation_history.append({"role": "user", "content": user_input})
            response = get_ai_response(user_input, api_key, st.session_state.conversation_history)
            st.session_state.conversation_history.append({"role": "assistant", "content": response})

            st.session_state.chat_log.append(("You", user_input))
            st.session_state.chat_log.append(("Counsellor", response))
            
            # Clear the user input after sending the message
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
