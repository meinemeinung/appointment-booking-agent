from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import pandas as pd
from chatbot import ChatBot, OpenAIChatBot
from manager import AppointmentManager, CSVAppointmentManager
import traceback
from chat import generate_response

load_dotenv()

app = Flask(__name__)
manager = CSVAppointmentManager(os.getenv("APPOINTMENT_PATH"))
chatbot = OpenAIChatBot(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', {})
    user_input = message.get('content')
    chat_id = message.get('id')

    if not user_input or not chat_id:
        return jsonify({"error": "Invalid input"}), 400
    
    response = generate_response(chatbot, manager, user_input)
    
    return jsonify({"message":{"content": response, "id": chat_id}})

if __name__ == '__main__':
    host = os.getenv("FLASK_HOST", '127.0.0.1')
    port = int(os.getenv("FLASK_PORT", 8000))
    app.run(host=host, port=port)
