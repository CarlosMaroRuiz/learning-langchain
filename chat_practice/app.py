from langchain_openai import ChatOpenAI
import os
from utils import create_banner_ultra,CleanMarkdownParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from utils.art import SKULL_ART
def execute_app():
    create_banner_ultra("DeepSeek Chat",SKULL_ART)
    llm = ChatOpenAI(
        model="deepseek-chat",
        base_url="https://api.deepseek.com/",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )

    clean_output_parser = CleanMarkdownParser()
    #ese pipe es un lcel
    chain = llm | clean_output_parser

    chat_history = [
       SystemMessage(content="Eres un asistente que responde siempre de manera honesta sin endulzar o querer adular a la persona que le pregunta.")
    ]

    user_input = ""
    while True:
        user_input = input("\n\nUsuario: ")
        if user_input.lower() == "exit":
            break

        chat_history.append(HumanMessage(content=user_input))

        print("DeepSeek: ", end="")
        full_response = ""

        for chunk in chain.stream(chat_history):
            print(chunk, end="", flush=True)
            full_response += chunk
            
        chat_history.append(AIMessage(content=full_response))