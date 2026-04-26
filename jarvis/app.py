from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from utils import create_banner_ultra, CleanMarkdownParser
from utils.art import SKULL_ART
from utils.voice import speak
from utils.ear import listen, wake_word

SYSTEM_PROMPT = """Eres Jarvis, un asistente personal de voz que corre completamente en local y en privado.
Responde siempre en español, de forma concisa y directa. 
No uses markdown ni listas, solo texto plano que suene natural al ser leido en voz alta."""

SENTENCE_ENDINGS = {".", "!", "?", ";", ":"}

def stream_and_speak(chain, chat_history):
    full_response = ""
    sentence_buffer = ""

    print("Jarvis: ", end="", flush=True)

    for chunk in chain.stream(chat_history):
        print(chunk, end="", flush=True)
        full_response += chunk
        sentence_buffer += chunk

        if any(sentence_buffer.rstrip().endswith(p) for p in SENTENCE_ENDINGS):
            fragment = sentence_buffer.strip()
            if fragment:
                speak(fragment, wait=True)
            sentence_buffer = ""

    if sentence_buffer.strip():
        speak(sentence_buffer.strip(), wait=True)

    print()
    return full_response

def execute_jarvis():
    create_banner_ultra("Jarvis", SKULL_ART)

    llm = ChatOllama(
        model="phi3.5",
        temperature=0.7,
        keep_alive=0
    )
    parser = CleanMarkdownParser()
    chain = llm | parser

    chat_history = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]

    speak("Jarvis en linea. Di mi nombre para activarme.")

    while True:
        wake_word(keywords=["jarvis", "harvis", "yarvis", "garvis", "arvis"])
        speak("Si, dime.")

        user_input = listen()

        if not user_input:
            speak("No te escuche bien. Volvere a esperar.")
            continue

        print(f"\nTu: {user_input}")

        if "salir" in user_input.lower() or "apagarte" in user_input.lower():
            speak("Hasta luego, Carlos. Apagando.")
            break

        chat_history.append(HumanMessage(content=user_input))
        full_response = stream_and_speak(chain, chat_history)
        chat_history.append(AIMessage(content=full_response))
