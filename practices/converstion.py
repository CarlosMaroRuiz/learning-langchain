from langchain_core.messages import HumanMessage,SystemMessage
from langchain_core.messages import BaseMessage
from typing import List 

# tipamos nuestros mensajes gracias a basemessage
messages_list: List[BaseMessage] = [
    SystemMessage(content="Eres un asistente que responde siempre de manera honesta sin endulzar o querer adular a la persona que le pregunta."),
    HumanMessage(content="¿Por que el cielo es azul?"),
]