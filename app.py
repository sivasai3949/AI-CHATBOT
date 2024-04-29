import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import openai
import io
from PIL import Image

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API with your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/process_chat', methods=['POST'])
def process_chat():
    data = request.form
    user_input = data.get('user_input')
    image_file = request.files.get('image')
    audio_file = request.files.get('audio')

    if user_input:
        if image_file:
            # Process image
            image_data = image_file.read()
            result = process_image(image_data)
        elif audio_file:
            # Process audio
            audio_data = audio_file.read()
            result = process_audio(audio_data)
        else:
            # Regular text input
            result = get_ai_response(user_input)

        return result

    return "Invalid input"

def get_ai_response(input_text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text}
        ]
    )
    return completion.choices[0].message['content']

def process_image(image_data):
    # Process the image data here
    # You can use image processing libraries like OpenCV or send the image to an external service
    # For example, if using PIL to resize the image:
    image = Image.open(io.BytesIO(image_data))
    resized_image = image.resize((224, 224))
    return "Image processed successfully"

def process_audio(audio_data):
    # Process the audio data here
    # You can use speech recognition libraries or send the audio to an external service
    # For example, if using OpenAI's Speech-to-Text API:
    result = openai.File.create(file=audio_data, purpose='transcription')
    transcription = result.transcription
    return transcription

if __name__ == '__main__':
    app.run(debug=True)
