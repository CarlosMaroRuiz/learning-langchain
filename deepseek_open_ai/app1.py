# usaremos los nuevos modelos de deepseek
from .utils import build_model,Chat


def execute_app():
    #instanciamos nuestro cliente
    client = build_model()
    chat = Chat(client)
    response = chat.create_chat("Hola, ¿cómo estás?")
    print(response.choices[0].message.content)


