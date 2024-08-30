# resolver/ai/base_ai.py
class BaseAI:
    def __init__(self):
        pass

    def process_message(self, message):
        raise NotImplementedError("Subclasses must implement this method")

    def initiate_microservice(self, service_name):
        raise NotImplementedError("Subclasses must implement this method")
