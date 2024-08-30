# resolver/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .ai.ai_model_1 import AIModel1

class ResolverConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connection established")
        self.ai_model = AIModel1()  # Initialize AI model
        await self.accept()

    async def disconnect(self, close_code):
        print("WebSocket connection closed")

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            print(f"Received text data: {text_data}")
            try:
                data = json.loads(text_data)
                message = data.get('message')

                if message:
                    response = self.ai_model.process_message(message)
                    await self.send(text_data=json.dumps(response))
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                await self.send(text_data=json.dumps({
                    'error': 'Invalid JSON received'
                }))
        else:
            print("No text data received")
