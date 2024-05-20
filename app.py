import streamlit as st
import requests
import json

# Define the HTML template for the chatbot
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Counsellor</title>
    <style>
        body {
          font-family: Arial, sans-serif;
          background-color: #f0f0f0;
          margin: 0;
          padding: 0;
        }
        .chatbot-container {
          max-width: 500px;
          margin: 50px auto;
          background-color: #fff;
          border-radius: 10px;
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
          padding: 20px;
        }
        header {
          display: flex;
          align-items: center;
        }
        .heading {
          margin: 0;
          font-size: 36px;
          font-family: 'Times New Roman', serif;
          background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
          color: transparent; /* Make the text transparent */
          -webkit-background-clip: text; /* For WebKit-based browsers */
          background-clip: text; /* Standard property for other browsers */
        }
        .robot-icon {
          width: 40px;
          margin-left: 10px;
        }
        .chat-container {
          height: 300px;
          overflow-y: auto;
          margin-top: 20px;
        }
        .chat {
          display: flex;
          flex-direction: column;
        }
        .chat-bubble {
          max-width: 70%;
          margin-bottom: 10px;
          padding: 10px;
          border-radius: 20px;
        }
        .user {
          align-self: flex-end;
          background-color: #007bff;
          color: #fff;
        }
        .robot {
          align-self: flex-start;
          background-color: #f0f0f0;
          color: #333;
        }
        .input-container {
          display: flex;
          margin-top: 20px;
        }
        input[type="text"] {
          flex: 1;
          padding: 10px;
          border: none;
          border-radius: 20px;
          margin-right: 10px;
        }
        #send-btn {
          background-color: #007bff;
          color: #fff;
          border: none;
          border-radius: 20px;
          padding: 10px 20px;
          cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="chatbot-container">
        <header>
            <h1 class="heading"><span>A</span><span>I</span> <span>C</span><span>O</span><span>U</span><span>N</span><span>S</span><span>E</span><span>L</span><span>L</span><span>O</span><span>R</span></h1>
            <img src="https://via.placeholder.com/40" alt="Robot Icon" class="robot-icon">
        </header>
        <div class="chat-container" id="chat-container">
            <div class="chat" id="chat">
                <div class="chat-bubble robot">Hi there! How can I assist you today?</div>
            </div>
        </div>
        <div class="input-container">
            <input type="text" id="user-input" placeholder="Type your message...">
            <button id="send-btn">Send</button>
        </div>
    </div>
</body>
</html>
"""

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
    st.title("AI Counsellor")

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]
        st.session_state.chat_log = []

    api_key = st.secrets["OPENAI_API_KEY"]  # Retrieve API key from Streamlit Secrets

    # Display the custom HTML
    st.components.v1.html(html_template, height=600)

    # JavaScript code to handle user input and button click
    st.write("""
        <script>
            document.getElementById('send-btn').addEventListener('click', function(event) {
                var userInput = document.getElementById('user-input').value;
                if (userInput) {
                    var chatContainer = document.getElementById('chat');
                    var userMessage = document.createElement('div');
                    userMessage.className = 'chat-bubble user';
                    userMessage.innerText = userInput;
                    chatContainer.appendChild(userMessage);

                    fetch('/send_message', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({user_input: userInput}),
                    })
                    .then(response => response.json())
                    .then(data => {
                        var botMessage = document.createElement('div');
                        botMessage.className = 'chat-bubble robot';
                        botMessage.innerText = data.response;
                        chatContainer.appendChild(botMessage);
                        chatContainer.scrollTop = chatContainer.scrollHeight;
                        document.getElementById('user-input').value = '';
                    });
                }
            });

            document.getElementById('user-input').addEventListener('keypress', function(event) {
                if (event.keyCode === 13) {
                    document.getElementById('send-btn').click();
                }
            });
        </script>
    """, unsafe_allow_html=True)

    if 'user_input' in st.experimental_get_query_params():
        user_input = st.experimental_get_query_params()['user_input'][0]
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        response = get_ai_response(user_input, api_key, st.session_state.conversation_history)
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
        st.session_state.chat_log.append(("You", user_input))
        st.session_state.chat_log.append(("Counsellor", response))

if __name__ == "__main__":
    main()
