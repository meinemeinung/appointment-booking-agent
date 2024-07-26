from abc import ABC, abstractmethod
import datetime as dt

class ChatBot(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def extract_entities_intent_dates(self, text):
        pass

    def process_details(self, details):
        clean_details = {}
        for key, val in details.items():
            if val.lower() != 'unknown':
                if key == 'date':
                    if val.lower() == 'today':
                        clean_details[key] = dt.datetime.today().date()
                    elif val.lower() == 'tomorrow':
                        clean_details[key] = dt.datetime.today().date() + dt.timedelta(days=1)
                    elif val.lower() == 'next week':
                        clean_details[key] = dt.datetime.today().date() + dt.timedelta(days=7)
                    else:
                        clean_details[key] = dt.datetime.strptime(val, '%Y-%m-%d').date()
                elif key in ['start_time', 'end_time']:
                    clean_details[key] = dt.datetime.strptime(
                        f'{clean_details["date"].strftime("%Y-%m-%d")} {details[key]}', '%Y-%m-%d %H:%M:%S'
                    )
                else:
                    clean_details[key] = val
            else:
                clean_details[key] = None
        return clean_details