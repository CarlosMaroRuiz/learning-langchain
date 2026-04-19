from langchain_openai import ChatOpenAI
import os
from utils import create_banner_ultra
from utils.art import ANIME_1
def execute_app():
    create_banner_ultra("DeepSeek Chat",ANIME_1)
    llm = ChatOpenAI(
        model="deepseek-chat",
        base_url="https://api.deepseek.com/",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )
