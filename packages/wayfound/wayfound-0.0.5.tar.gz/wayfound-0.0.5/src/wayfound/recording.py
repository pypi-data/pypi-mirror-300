import os
import requests
import json

# https://packaging.python.org/en/latest/tutorials/packaging-projects/

class Recording:
    WAYFOUND_RECORDINGS_URL = "https://app.wayfound.ai/api/v1/recordings/active"

    def __init__(self, wayfound_api_key=None, agent_id=None, initial_messages=[]):
        super().__init__()

        self.wayfound_api_key = wayfound_api_key or os.getenv("WAYFOUND_API_KEY")
        self.agent_id = agent_id or os.getenv("WAYFOUND_AGENT_ID")
        
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.wayfound_api_key}"
        }

        payload = {
            "agentId": self.agent_id,
            "messages": initial_messages
        }

        try:
            response = requests.post(self.WAYFOUND_RECORDINGS_URL, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            response_data = response.json()
            self.recording_id = response_data['id']
        except requests.exceptions.RequestException as e:
            print(f"Error during POST request: {e}")
            self.recording_id = None

    def record_messages(self, messages):
        payload = {
            "recordingId": self.recording_id,
            "messages": messages
        }

        try:
            response = requests.put(self.WAYFOUND_RECORDINGS_URL, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error during PUT request: {e}")

    def record_messages_from_langchain_memory(self, memory):
        formatted_messages = []
        for message in memory.chat_memory.messages:
            if message.type == 'ai':
                formatted_messages.append({'role': 'assistant', 'content': message.content})
            elif message.type == 'human':
                formatted_messages.append({'role': 'user', 'content': message.content})

        self.record_messages(formatted_messages)