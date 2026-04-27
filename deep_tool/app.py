from .build_model import build_model
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from .tools import get_weather
from langchain_core.tools import BaseTool
from .utils import info_tool_using

TOOLS_MAP: dict[str, BaseTool] = {
    "get_weather": get_weather,
}

def execute():
    model: ChatOpenAI = build_model()
    model_with_tools = model.bind_tools([get_weather])

    messages = [{"role": "user", "content": "¿Cuál es el clima en Madrid hoy?"}]

    ai_message = model_with_tools.invoke(messages)
    messages.append(ai_message)
    info_tool_using(ai_message)
    print("ai_message:", ai_message.content)

    if ai_message.tool_calls:
        for tool_call in ai_message.tool_calls:
            tool_fn = TOOLS_MAP[tool_call["name"]]
            result = tool_fn.invoke(tool_call)
            #se manda el resultado de la funcion que ejecuto
            messages.append(ToolMessage(
                content=result,
                tool_call_id=tool_call["id"],
            ))

    final_response = model_with_tools.invoke(messages)
    print(final_response.content)