from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from chatbot import ChatBot, OpenAIChatBot
from manager import AppointmentManager, CSVAppointmentManager
import traceback

load_dotenv()

app = Flask(__name__)
manager = CSVAppointmentManager(os.getenv("APPOINTMENT_PATH"))
chatbot = OpenAIChatBot(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(chatbot: ChatBot, appointment_manager: AppointmentManager, user_input: str):
    try:
        details = chatbot.extract_entities_intent_dates(user_input)
        intent = details['intention'].lower()
        if not intent:
            response = "Sorry, I didn't understand that. Could you state your intention (create or check) an appointment"
        elif intent == 'create':
            exit_code, response = appointment_manager.create_appointment(
                entity=details['entity'],
                start=details['start_time'],
                end=details['end_time']
            )
            if exit_code == 2:
                appointment_list = appointment_manager.read_appointment(
                    date=details['date']
                )
                response += f"\nHere are the list of appointments on {details['date']}\n"
                response += appointment_list.to_string()
        elif intent == 'read':
            appointment_list = appointment_manager.read_appointment(
                date=details['date']
            )
            response = f"Here are the list of appointments on {details['date']}\n"
            response += appointment_list.to_string()
        else:
            response = f"Sorry, we are currently unable to process {intent} via chatbot."
    except Exception as e:
        print(traceback.format_exc())
        response = "Sorry, I didn't understand that. Could you state your intention (create or check) an appointment"

    return response

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
