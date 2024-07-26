# from flask import Flask, request, jsonify, render_template
import traceback
import pandas as pd
from chatbot import ChatBot
from manager import AppointmentManager


def format_appoinment_list(appointment: pd.DataFrame) -> str:
    appointment['Start'] = appointment['Start'].dt.strftime('%H:%M:%S')
    appointment['End'] = appointment['End'].dt.strftime('%H:%M:%S')
    appointment = appointment[['Start', 'End']]
    return appointment.to_string(header=None, index=None)

def get_read_response(appointment_manager: AppointmentManager, details):
    appointment_list = appointment_manager.read_appointment(
        date=details['date']
    )
    response = f"\nHere are the list of appointments on {details['date'].strftime('%d %B %Y')}\n\n"
    response += format_appoinment_list(appointment_list)

    return response

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
                response += get_read_response(appointment_manager, details)
        elif intent == 'read':
            response = get_read_response(appointment_manager, details)
        else:
            response = f"Sorry, we are currently unable to process {intent} via chatbot."
    except Exception as e:
        print(traceback.format_exc())
        response = "Sorry, I didn't understand that. Could you state your intention (create or check) an appointment"

    return response
