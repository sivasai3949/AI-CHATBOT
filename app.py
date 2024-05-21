import streamlit as st
import requests
import json

def get_ai_response(input_text, api_key, conversation_history):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer " + api_key,
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": conversation_history + [
            {"role": "user", "content": input_text}
        ],
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error: Failed to get response from OpenAI API"

def main():
    st.title("AI Counsellor")

    # Initialize conversation history if not already present
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "assistant", "content": "Hello! I'm here to help. How may I assist you today?"}
        ]
        st.session_state.chat_log = [
            ("Counsellor", "Hello! I'm here to help. How may I assist you today?")
        ]

    # Display the conversation history
    st.markdown(
        "<style>.user-bubble { background-color: #e6f7ff; padding: 10px; border-radius: 5px; margin-bottom: 10px; } "
        ".counsellor-bubble { background-color: #f1f1f1; padding: 10px; border-radius: 5px; margin-bottom: 10px; }</style>",
        unsafe_allow_html=True
    )

    for sender, message in st.session_state.chat_log:
        if sender == "You":
            st.markdown(f"<div class='user-bubble'><strong>You:</strong> {message}</div>", unsafe_allow_html=True)
        elif sender == "Counsellor":
            st.markdown(f"<div class='counsellor-bubble'><strong>Counsellor:</strong> {message}</div>", unsafe_allow_html=True)

    # Input field for the user's message
    user_input = st.text_input("Your message here...", key="input")

    api_key = st.secrets["OPENAI_API_KEY"]  # Retrieve API key from Streamlit Secrets

    if st.button("Send"):
        if user_input:
            # Add user's message to the conversation history and chat log
            st.session_state.conversation_history.append({"role": "user", "content": user_input})
            st.session_state.chat_log.append(("You", user_input))
            
            # Get the AI response
            response = get_ai_response(user_input, api_key, st.session_state.conversation_history)
            
            # Add AI's response to the conversation history and chat log
            st.session_state.conversation_history.append({"role": "assistant", "content": response})
            st.session_state.chat_log.append(("Counsellor", response))
            
            # Clear the input field
            st.session_state.input = ""

if __name__ == "__main__":
    main()
