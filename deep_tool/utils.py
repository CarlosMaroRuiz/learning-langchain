from langchain_core.messages import AIMessage

def info_tool_using(ai_message: AIMessage) -> None:
    print("Herramientas que el modelo usara para completar la operacion:")
    for tool_call in ai_message.tool_calls:
        print(f"- {tool_call['name']}")