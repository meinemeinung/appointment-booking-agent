import datetime as dt
import os
from dotenv import load_dotenv
from chatbot import ChatBot, OpenAIChatBot
from manager import AppointmentManager, CSVAppointmentManager

def get_user_input() -> str:
    return input("You: ")

def handle_exit(user_input: str) -> bool:
    return user_input.lower() == 'exit'

def generate_response(chatbot: ChatBot, appointment_manager: AppointmentManager, user_input: str):
    try:
        details = chatbot.extract_entities_intent_dates(user_input)
        intent = details['intention'].lower()
        if not intent:
            response = "Sorry, I didn't understand that. Could you state your intention (create or check) an appointment"
        elif intent=='create':
            exit_code, response = appointment_manager.create_appointment(
                entity=details['entity'],
                start=details['start_time'],
                end=details['end_time']
                )
            if exit_code==2:
                appointment_list = appointment_manager.read_appointment(
                    date=details['date']
                    )
                response += f"\nHere are the list of appointments on {details['date']}\n"
                response += appointment_list.to_string()
        elif intent=='read':
            appointment_list = appointment_manager.read_appointment(
                date=details['date']
                )
            response = f"Here are the list of appointments on {details['date']}\n"
            response += appointment_list.to_string()
        else:
            response = f"Sorry, we are currently unable to process {intent} via chatbot."
    except Exception as e:
        print(e)
        response = "Sorry, I didn't understand that. Could you state your intention (create or check) an appointment"
    
    return response

def chat(chatbot: ChatBot, appointment_manager: AppointmentManager):
    print("Welcome to the Appointment Booking Chatbot!")
    print("You can type 'exit' at any time to end the conversation.")
    
    while True:
        user_input = get_user_input()
        if handle_exit(user_input):
            print("Chatbot: Goodbye!")
            break
        
        response = generate_response(chatbot, appointment_manager, user_input)
        print(f"Chatbot: {response}")

if __name__ == '__main__':
    load_dotenv()
    manager = CSVAppointmentManager(os.getenv("APPOINTMENT_PATH"))
    chatbot = OpenAIChatBot(api_key=os.getenv("OPENAI_API_KEY"))
    chat(chatbot, manager)
    