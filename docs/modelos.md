# Modelos llm

## Trabajando con el modelo de deepseek via api

Para trabajar con este modelo es necesario instalar la libreria "langchain-openai"

```bash
uv add langchain-openai
uv add python-dotenv
```

una vez estado en nuestro codigo python , debemos importar el modelo de la siguiente manera:
```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(base_url="https://api.deepseek.com/", api_key="api-key", model="deepseek-chat")
```
como buenas practicas se debe usar variables de entorno para guardar las api-keys. en este caso utilizaremos dotenv para cargarlas.


## SystemMessage y HumanMessage

que es cada uno de ellos , en que se diferencian , y como se utilizan en langchain.

# SystemMessage

El SystemMessage es una clase de langchain que se utiliza para enviar mensajes al modelo.
su sintaxis es la siguiente:

```python
from langchain_core.messages import SystemMessage

system_message = SystemMessage(content="Eres un asistente sarcástico pero muy inteligente.")
```
Esto es util para definir el comportamiento del modelo, su personalidad,etc.
# HumanMessage

El HumanMessage es una clase de langchain que se utiliza para enviar mensajes al modelo.
su sintaxis es la siguiente:

```python
from langchain_core.messages import HumanMessage

human_message = HumanMessage(content="¿Por qué el cielo es azul en 20 palabras?")
```
esto es utile para enviar mensajes al modelo, su funcion es enviar las preguntas, que queremos que el modelo realice. 


# trabajando con llm.invoke y llm.stream

para enviar un mensaje al modelo se puede utilizar el metodo invoke.
su sintaxis es la siguiente:

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOpenAI(base_url="https://api.deepseek.com/", api_key="api-key", model="deepseek-chat")

messages = [
    SystemMessage(content="Eres un asistente sarcástico pero muy inteligente."),
    HumanMessage(content="¿Por qué el cielo es azul en 20 palabras?"),
]

response = llm.invoke(messages)
print(response.content)
```

para enviar un mensaje al modelo se puede utilizar el metodo stream.
su sintaxis es la siguiente:

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOpenAI(base_url="https://api.deepseek.com/", api_key="api-key", model="deepseek-chat")

messages = [
    SystemMessage(content="Eres un asistente sarcástico pero muy inteligente."),
    HumanMessage(content="¿Por qué el cielo es azul en 20 palabras?"),
]

for chunk in llm.stream(messages):
    print(chunk.content, end="", flush=True)
```
la diferencia fundamental entre ambos es que invoke nos da la respuesta completa de una vez , mientras que stream nos da la respuesta poco a poco.


## AIMessage

A diferencia del `SystemMessage` y `HumanMessage` que enviamos nosotros, **`AIMessage` es la clase que devuelve el modelo** como respuesta (o que usamos nosotros para simular el historial de una conversación pasada).

Cuando imprimes el objeto completo, contiene varios datos técnicos útiles. Para no saturarte, estos son los esenciales:

*   **`content`**: El texto real generado por la IA (la respuesta que ve el usuario). Es lo que debes extraer (`response.content`) para limpiar la consola.
*   **`response_metadata`**: Datos crudos de la API del proveedor, como el modelo usado (`model_name`) o por qué dejó de escribir (`finish_reason`).
*   **`usage_metadata`**: Un contador estandarizado de cuántos "tokens" (palabras/costo) gastaste en la entrada y en la salida.
*   **`tool_calls`**: Si le enseñaste herramientas a la IA (ej. buscar en Google), y la IA decidió usarlas, aquí vendrá el nombre de la herramienta a ejecutar y sus variables.
*   **`id`**: Un identificador único del mensaje, útil si guardas la charla en una base de datos.
