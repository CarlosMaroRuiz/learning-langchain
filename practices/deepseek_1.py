from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
#dependencias internas
from .converstion import messages_list
load_dotenv()

def execute():
    llm = ChatOpenAI(
        model="deepseek-chat",
        base_url="https://api.deepseek.com/",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )
    response = llm.invoke(messages_list)
    print(response)

