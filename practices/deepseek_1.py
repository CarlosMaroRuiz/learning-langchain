from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from utils import CleanMarkdownParser
#dependencias internas
from .converstion import messages_list
load_dotenv()

llm = ChatOpenAI(
        model="deepseek-chat",
        base_url="https://api.deepseek.com/",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )
def execute():
 
    response = llm.invoke(messages_list)
    print(response)


def execute_async():
    chain = llm | CleanMarkdownParser()
    for message in chain.stream(messages_list):
        print(message, end="", flush=True)
