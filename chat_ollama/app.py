from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from utils import create_banner_ultra, CleanMarkdownParser
from utils.art import SKULL_ART

def execute_ollama_app():

    create_banner_ultra("Agente Local", SKULL_ART)
 
    llm = ChatOllama(
        model="deepseek-r1:1.5b",
        temperature=0.7
    )
    clean_output_parser = CleanMarkdownParser()
    chain = llm | clean_output_parser

 
    chat_history = [
        SystemMessage(content="Eres un asistente muy útil que procesa todo localmente de forma privada en el ordenador del usuario.")
    ]

 
    user_input = ""
    while True:
        user_input = input("\n\nUsuario: ")
        if user_input.lower() == "exit":
            break

        chat_history.append(HumanMessage(content=user_input))

        print("Local-IA: ", end="")
        full_response = ""
        

        for chunk in chain.stream(chat_history):
            print(chunk, end="", flush=True)
            full_response += chunk
            
        chat_history.append(AIMessage(content=full_response))
