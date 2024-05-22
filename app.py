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

    user_input = st.text_input("Type your message...")

    api_key = st.secrets["OPENAI_API_KEY"]  # Retrieve API key from Streamlit Secrets

    if st.button("Send"):
        if user_input:
            st.session_state.conversation_history.append({"role": "user", "content": user_input})
            response = get_ai_response(user_input, api_key, st.session_state.conversation_history)
            st.session_state.conversation_history.append({"role": "assistant", "content": response})

            st.session_state.chat_log.append(("You", user_input))
            st.session_state.chat_log.append(("Counsellor", response))

    # Display the conversation history
    for sender, message in st.session_state.chat_log:
        if sender == "You":
            st.write(f"You: {message}")
        elif sender == "Counsellor":
            st.write(f"Counsellor: {message}")

if __name__ == "__main__":
    main()



