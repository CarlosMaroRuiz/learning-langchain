from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

def build_model():
    client = OpenAI(
        base_url="https://api.deepseek.com",
        api_key=api_key
    )
    return client





class Chat:
    def __init__(self, client:OpenAI):
        self.client = client
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    def create_chat(self, message):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages + [{"role": "user", "content": message}]
        )
        return response
