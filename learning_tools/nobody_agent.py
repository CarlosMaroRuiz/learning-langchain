from langchain_core.tools import tool
from langchain_core.messages import ToolMessage


@tool
def get_weather(location: str) -> str:
    """Obtiene el clima de una ubicación."""  
    return f"El clima en {location} es soleado."

def execute():
    # Esto es lo que retorna un modelo cuando usa una tool
    tool_call = {
        "name": "get_weather",
        "args": {"location": "Madrid"},
        "id": "1234",
    }
    
    # Ejecutamos la tool el modelo pasa el arg
    result = get_weather.invoke(tool_call["args"])
    
    tool_message = ToolMessage(
        content=result,
        tool_call_id=tool_call["id"],
    )
    
    print(tool_message)

if __name__ == "__main__":
    execute()