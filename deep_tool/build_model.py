from __future__ import annotations
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def build_model() -> ChatOpenAI:
    api_key: str | None = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("Falta DEEPSEEK_API_KEY en el entorno")

    llm: ChatOpenAI = ChatOpenAI(
        model="deepseek-v4-flash",
        base_url="https://api.deepseek.com",
        api_key=api_key,
        model_kwargs={
            "extra_body": {"thinking": {"type": "disabled"}}
        },
    )
    return llm
