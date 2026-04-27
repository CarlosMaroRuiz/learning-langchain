from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from typing import Any, Dict



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
        raise RuntimeError("Ocurrió un error crítico durante la búsqueda.")
    return f"Resultados de la búsqueda para: {query}"

tools_map = {
    "divide": divide,
    "search_web": search_web
}

# ---UTILIDAD DE MANEJO DE ERRORES ---

def tool_executor(tool_call: Dict[str, Any]) -> ToolMessage:
    name = tool_call["name"]
    args = tool_call["args"]
    call_id = tool_call["id"]
    
    
    selected_tool = tools_map.get(name)
    
    try:
        if not selected_tool:
            raise NameError(f"La herramienta '{name}' no existe.")
            
        output = selected_tool.invoke(args)
        
    except Exception as e:

        output = f"Error en la ejecución: {str(e)}"
    
    return ToolMessage(content=str(output), tool_call_id=call_id)


if __name__ == "__main__":
   
    llamadas_del_modelo = [
        {"name": "divide", "args": {"a": 10, "b": 0}, "id": "call_001"},       # Error División
        {"name": "search_web", "args": {"query": "LangChain"}, "id": "call_002"}, # Éxito
        {"name": "search_web", "args": {"query": "error"}, "id": "call_003"},     # Error Búsqueda
        {"name": "volar_avion", "args": {"altitud": 500}, "id": "call_004"}      # Error No existe
    ]

    print("--- PROCESANDO HERRAMIENTAS ---\n")
    
    respuestas = []
    for call in llamadas_del_modelo:
        mensaje_resultado = tool_executor(call)
        respuestas.append(mensaje_resultado)
        
    
        status = "error" if "Error" in mensaje_resultado.content else "correcto"
        print(f"{status} ID: {mensaje_resultado.tool_call_id}")
        print(f"   Contenido: {mensaje_resultado.content}\n")

