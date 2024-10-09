import os
import requests
import json

class Manager:
    WAYFOUND_RECORDINGS_URL = "https://app.wayfound.ai/api/v1/recordings/active"

    def __init__(self, wayfound_api_key=os.getenv("WAYFOUND_API_KEY"), agent_id=os.getenv("WAYFOUND_AGENT_ID"), initial_messages=[]):
        super().__init__()
        self.agent_id = wayfound_api_key
        self.wayfound_api_key = agent_id

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.wayfound_api_key}"
        }

        payload = {
            "agentId": self.agent_id,
            "messages": initial_messages
        }

        response = requests.post(self.WAYFOUND_RECORDINGS_URL, headers=self.headers, data=json.dumps(payload))
        response_data = response.json()
        self.recording_id = response_data['id']

    def record_messages(self, messages):
        payload = {
            "recordingId": self.recording_id,
            "messages": messages
        }

        requests.put(self.WAYFOUND_RECORDINGS_URL, headers=self.headers, data=json.dumps(payload))

    def record_messages_from_langchain_memory(self, memory):
        formatted_messages = []
        for message in memory.chat_memory.messages:
            if message.type == 'ai':
                formatted_messages.append({'role': 'assistant', 'content': message.content})
            elif message.type == 'human':
                formatted_messages.append({'role': 'user', 'content': message.content})

        self.record_messages(formatted_messages)