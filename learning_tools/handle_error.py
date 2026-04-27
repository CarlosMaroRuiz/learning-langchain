from langchain_core.tools import tool
from langchain_core.messages import ToolMessage

@tool
def divide(a: float, b: float) -> float:
    """Divide dos números."""
    if b == 0:
        raise ValueError("No se puede dividir por cero.")
    return a / b

@tool
def search_web(query: str) -> str:
    """Simula una búsqueda en la web."""
    if "error" in query.lower():
        raise RuntimeError("Ocurrió un error durante la búsqueda.")
    return f"Resultados de la búsqueda para: {query}"

# Probamos la división por cero
tool_call_div_zero = {"name": "divide", "args": {"a": 10, "b": 0}, "id": "call_div"}
try:
    result_div = divide.invoke(tool_call_div_zero["args"])
except Exception as e:
    result_div = f"Error: {str(e)}"
msg_div = ToolMessage(content=result_div, tool_call_id=tool_call_div_zero["id"])

# Probamos la búsqueda en la web
tool_call_err = {"name": "search_web", "args": {"query": "provocar error"}, "id": "call_err"}
try:
    result_err = search_web.invoke(tool_call_err["args"])
except Exception as e:
    result_err = f"Error: {str(e)}"
msg_err = ToolMessage(content=result_err, tool_call_id=tool_call_err["id"])

print("msg_div:", msg_div)
print("msg_err:", msg_err)