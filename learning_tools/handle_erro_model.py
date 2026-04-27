from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com/",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

@tool
def divide(a: float, b: float) -> float:
    """Divide dos números."""
    if b == 0:
        raise ValueError("No se puede dividir por cero.")
    return a / b

llm_with_tools = llm.bind_tools([divide])

messages = [
    SystemMessage(content="Eres un asistente que usa herramientas."),
    HumanMessage(content="Divide 10 entre 0"),
]

response = llm_with_tools.invoke(messages)
messages.append(response)


tool_call = response.tool_calls[0]
try:
    result = divide.invoke(tool_call["args"])
except Exception as e:
    result = f"Error: {str(e)}"

messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))


final = llm_with_tools.invoke(messages)
print(final.content) 