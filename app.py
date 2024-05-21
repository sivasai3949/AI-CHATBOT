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

def submit_input():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        response = get_ai_response(user_input, st.secrets["OPENAI_API_KEY"], st.session_state.conversation_history)
        st.session_state.conversation_history.append({"role": "assistant", "content": response})

        st.session_state.chat_log.append(("You", user_input))
        st.session_state.chat_log.append(("Counsellor", response))
        
        # Clear the input field
        st.session_state.user_input = ""

def main():
    st.title("AI COUNSELLOR")
    st.write("Hi there! How can I assist you today?")

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]
        st.session_state.chat_log = []

    # Add a text input field with on_change callback
    st.text_input("Type your message...", key="user_input", on_change=submit_input)

    if st.button("Send"):
        submit_input()

    # Display the conversation history
    st.markdown("<style>.user-bubble { background-color: #e6f7ff; padding: 10px; border-radius: 5px; margin-bottom: 10px; } .counsellor-bubble { background-color: #f1f1f1; padding: 10px; border-radius: 5px; margin-bottom: 10px; }</style>", unsafe_allow_html=True)
    
    for sender, message in st.session_state.chat_log:
        if sender == "You":
            st.markdown(f"<div class='user-bubble'><strong>You:</strong> {message}</div>", unsafe_allow_html=True)
        elif sender == "Counsellor":
            st.markdown(f"<div class='counsellor-bubble'><strong>Counsellor:</strong> {message}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
