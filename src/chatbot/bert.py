from .base import ChatBot

class BertChatBot(ChatBot):
    def __init__(self, model_path):
        super().__init__()
        self.model_path = model_path

    def extract_entities_intent_dates(self, text: str):
        raise NotImplementedError()