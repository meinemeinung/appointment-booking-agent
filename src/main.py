import datetime as dt
import os
from dotenv import load_dotenv
from chatbot import ChatBot, OpenAIChatBot
from manager import AppointmentManager, CSVAppointmentManager
from chat import generate_response

def get_user_input() -> str:
    return input("You: ")

def handle_exit(user_input: str) -> bool:
    return user_input.lower() == 'exit'

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
    