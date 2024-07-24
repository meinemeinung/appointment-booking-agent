from abc import ABC, abstractmethod

class ChatBot(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def extract_entities_intent_dates(self, text):
        pass

    