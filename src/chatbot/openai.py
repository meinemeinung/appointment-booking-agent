import datetime as dt
from openai import OpenAI
from .base import ChatBot

class OpenAIChatBot(ChatBot):
    def __init__(self, api_key, model="gpt-4o"):
        self.__api_key = api_key
        self.model = model

    def __get_chat_completion(self, text: str):
        client = OpenAI(api_key=self.__api_key)
        messages = [
            {"role": "system", "content": "You are an appointment booking agent"},
            {"role": "user", "content": text}
            ]
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content        

    def extract_entities_intent_dates(self, text: str):
        output = self.__get_chat_completion(
            "Extract the entity, intention, date, start_time and end_time details from the text. " + 
            "Return the details in the form ENTITY,INTENTION,DATE,START_TIME,END_TIME " + 
            "Rules for ENTITY is as follows: " +
            "entity is the person or object the meeting is scheduled with" + 
            "Rules for INTENTION is as follows: " +
            "intention is the action to be taken, mapped to one of CRUD (Create, Read, Update, Delete). " +
            "Schedule, book, or set up a meeting -> Create " +
            "Check, view, or see an appointment -> Read " +
            "Reschedule, change, or modify an appointment -> Update " + 
            "Cancel, delete, or remove an appointment -> Delete " +
            "That's the rule for INTENTION." +
            "Rules for DATE is as follows: " +
            "Date is the date of the event in YYYY-MM-DD format " +
            "include understanding relative terms like 'today', 'tomorrow', 'next week'. " +
            "If the date is in relative terms, then leave them as 'today', 'tomorrow', 'next week'. " +
            "That's the rule for DATE." + 
            "Start Time: The start time of the event. Output in HH:MM:SS format. " +
            "End Time: The end time of the event. Output in HH:MM:SS format. " +
            "Leave all details that are unavailable from the text as string 'Unknown'."  + 
            "As an example, if the entity is Joe and the Date is 21 July 2024, while the intention, start_time and end_time are unknown " +
            "you should return Joe,Unknown,2024-07-21,Unknown,Unknown" +
            "Another example, if the intention is create and other information is not available, then return Unknown,create,Unknown,Unknown, " +
            "So there MUST be EXACTLY FOUR commas in your response. " +
            "If you cannot understand extract any information from the text, then just return Unknown,Unknown,Unknown,Unknown,Unknown. "+
            text
            )
        
        entity, intention, date, start_time, end_time = output.split(',')
        details = {
            'entity': entity.strip(),
            'intention': intention.strip(),
            'date': date.strip(),
            'start_time': start_time.strip(),
            'end_time': end_time.strip()
        }
        clean_details = {}
        for key,val in details.items():
            if val.lower() != 'unknown':
                if key=='date':
                    clean_details[key] = dt.datetime.strptime(val, '%Y-%m-%d')
                elif key in ['start_time', 'end_time']:
                    clean_details[key] = dt.datetime.strptime(f'{details["date"]} {details[key]}', '%Y-%m-%d %H:%M:%S')
                else:
                    clean_details[key] = val
            else:
                clean_details[key] = None

        return clean_details
    