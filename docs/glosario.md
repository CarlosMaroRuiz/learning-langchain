# Glosario de conceptos: LangChain y LLMs

---

## Conceptos generales de LLMs

### LLM (Large Language Model)
Modelo de lenguaje de gran escala entrenado sobre grandes volumenes de texto. Recibe texto como entrada y genera texto como salida prediciendo el siguiente token de manera probabilistica. Ejemplos: GPT-4o, Claude, Gemini, Llama.

### Chat Model
Variante de LLM optimizada para conversacion. En vez de recibir un string y devolver un string, recibe una lista de mensajes y devuelve un mensaje. En LangChain todas las clases de modelo con prefijo `Chat` (ej. `ChatOpenAI`) son chat models. No confundir con los LLMs de texto plano (completions), que estan en proceso de deprecacion.

### Token
Unidad basica de procesamiento de un LLM. No equivale exactamente a una palabra: puede ser una palabra, parte de una palabra, o un signo de puntuacion. El costo de uso y los limites de contexto se miden en tokens.

### Context window
Cantidad maxima de tokens que un modelo puede procesar en una sola llamada (entrada + salida combinadas). Si la conversacion supera este limite, el modelo no puede "ver" los mensajes mas antiguos. Modelos modernos tienen ventanas de 128K a 1M tokens.

### Temperature
Parametro que controla la aleatoriedad de las respuestas. `0` hace el modelo determinista (siempre elige el token mas probable). Valores altos producen respuestas mas creativas y variables. Para tareas de extraccion o codigo se recomienda `0` o cercano a `0`.

### Prompt
El texto o conjunto de mensajes que se envia al modelo como entrada. Incluye instrucciones, contexto, y la pregunta o tarea del usuario.

### System prompt
Mensaje especial que va al inicio de la conversacion y define el comportamiento del modelo: su rol, tono, restricciones, y cualquier instruccion que deba seguir en toda la sesion.

### Inference
El proceso de ejecutar un modelo para obtener una respuesta. Cada llamada a `model.invoke(...)` es una inferencia.

### Embedding
Representacion numerica de un texto en forma de vector de alta dimension. Textos con significado similar producen vectores cercanos en el espacio vectorial. Se usan para busqueda semantica, clustering y RAG.

### Hallucination
Fenomeno en el que un LLM genera informacion falsa o inventada con aparente confianza. Es una limitacion intrinseca del modelo, no un bug. Se mitiga con RAG, structured output y verificaciones externas.

---

## Componentes de LangChain

### Chat model (clase)
Clase de LangChain que envuelve la API de un proveedor de LLM. Todas implementan la misma interfaz: `invoke`, `stream`, `batch`, `bind_tools`, `with_structured_output`. Ejemplos: `ChatOpenAI`, `ChatAnthropic`, `ChatGoogleGenerativeAI`.

### `init_chat_model`
Funcion factory que instancia un chat model sin depender directamente de la clase del proveedor. Detecta el proveedor por el nombre del modelo o por el prefijo `provider:model`. Permite crear modelos configurables en runtime cuyo proveedor o modelo puede cambiarse en cada invocacion via `config`.

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4o", temperature=0)
```

### Message
Unidad fundamental de contexto para un modelo. Cada mensaje tiene un rol (`system`, `user`, `assistant`, `tool`) y un contenido (texto, imagenes, archivos, etc.). LangChain provee clases estandar que funcionan con todos los proveedores.

Tipos principales:
- `SystemMessage` — instrucciones de comportamiento para el modelo
- `HumanMessage` — input del usuario
- `AIMessage` — respuesta generada por el modelo, puede contener `tool_calls`
- `ToolMessage` — resultado de ejecutar una tool, incluye `tool_call_id` para correlacionarlo con la peticion

### Tool
Funcion Python con un schema bien definido (nombre, descripcion, argumentos) que se expone al modelo para que este decida cuando invocarla. El modelo no ejecuta la funcion directamente; genera un `tool_call` con los argumentos y es el codigo del desarrollador (o el agente) quien la ejecuta.

```python
from langchain.tools import tool

@tool
def buscar_clima(ciudad: str) -> str:
    """Obtiene el clima actual de una ciudad."""
    return f"22 grados en {ciudad}"
```

### `bind_tools`
Metodo disponible en cualquier chat model que soporte tool calling. Registra una lista de tools en el modelo para que este sepa que opciones tiene disponibles en cada invocacion.

```python
model_with_tools = model.bind_tools([buscar_clima])
```

### Tool calling
Mecanismo por el cual un LLM, en vez de responder con texto, responde con una solicitud estructurada para ejecutar una o varias tools. El modelo devuelve el nombre de la tool y los argumentos inferidos del contexto. Tambien llamado "function calling".

### `ToolRuntime`
Parametro especial inyectable en tools que da acceso a contexto de ejecucion: estado de la conversacion, store de larga duracion, configuracion del run, y capacidad de emitir updates en tiempo real (streaming parcial).

### Agent
Sistema que combina un modelo con tools en un loop. El modelo decide que tool usar, el agente la ejecuta, el resultado se devuelve al modelo, y el ciclo se repite hasta que el modelo emite una respuesta final o se alcanza un limite de iteraciones. En LangChain se construyen con `create_agent` (basado en LangGraph).

### `create_agent`
Funcion de alto nivel que crea un agente listo para produccion usando LangGraph internamente. Recibe un modelo, una lista de tools, y configuraciones opcionales como memoria, structured output, y middleware.

```python
from langchain.agents import create_agent

agent = create_agent("openai:gpt-4o", tools=[buscar_clima])
result = agent.invoke({"messages": [{"role": "user", "content": "Clima en Tuxtla?"}]})
```

### Structured output
Capacidad de forzar que el modelo retorne datos en un formato especifico (JSON, Pydantic model, dataclass) en vez de texto libre. Se usa `with_structured_output` en el modelo o `response_format` en `create_agent`. Util para extraccion de datos, clasificacion, y cualquier tarea donde la salida debe ser parseada por codigo.

```python
from pydantic import BaseModel

class Contacto(BaseModel):
    nombre: str
    email: str

structured_model = model.with_structured_output(Contacto)
```

### Retriever
Interfaz que, dada una query en lenguaje natural, devuelve una lista de documentos relevantes. Es la pieza central del pipeline de RAG. Puede estar respaldado por un vector store, una base de datos SQL, una API, o cualquier fuente de datos.

### Vector store
Base de datos especializada en almacenar embeddings y realizar busquedas de similitud semantica. Dados un embedding de consulta, devuelve los documentos cuyo embedding este mas cercano en el espacio vectorial. Ejemplos: Chroma, Pinecone, FAISS, pgvector.

### Document loader
Componente que ingesta datos de fuentes externas (PDFs, Google Drive, Slack, Notion, paginas web) y los convierte en objetos `Document` estandar de LangChain.

### Text splitter
Componente que divide documentos grandes en chunks mas pequenos antes de generar sus embeddings. Es necesario porque los modelos de embedding tienen su propio limite de tokens y porque chunks mas pequenos permiten recuperacion mas precisa en RAG.

---

## Patrones y arquitecturas

### RAG (Retrieval-Augmented Generation)
Arquitectura que combina recuperacion de documentos con generacion de texto. En vez de depender solo del conocimiento del modelo, se recuperan fragmentos relevantes de una base de conocimiento externa y se pasan como contexto al LLM. Resuelve dos limitaciones del LLM: conocimiento estatico y ventana de contexto finita.

Variantes:
- **2-Step RAG** — la recuperacion siempre ocurre antes de la generacion. Simple y predecible.
- **Agentic RAG** — el agente decide cuando y como recuperar durante el razonamiento. Mas flexible, latencia variable.

### Short-term memory (memoria de corto plazo)
Persistencia del historial de mensajes dentro de una misma sesion o thread. Se implementa con un `checkpointer` que guarda el estado del agente en cada paso. En desarrollo se usa `InMemorySaver`; en produccion, `PostgresSaver` u otro backend.

### Long-term memory (memoria de largo plazo)
Informacion que persiste entre distintas sesiones y threads. Se almacena en un `Store` externo y se recupera cuando es relevante. Util para preferencias de usuario, historial de interacciones pasadas, y conocimiento acumulado.

### Checkpointer
Componente que serializa y persiste el estado del agente (incluyendo el historial de mensajes) en cada paso del grafo. Permite reanudar conversaciones y hacer time-travel debugging. Requerido para que un agente tenga memoria de corto plazo.

### Thread
Unidad de organizacion de una conversacion. Agrupa multiples interacciones en una sesion identificada por un `thread_id`. El agente puede mantener contexto entre mensajes del mismo thread.

### LCEL (LangChain Expression Language)
Sistema de composicion de componentes usando el operador `|`. Permite encadenar un prompt, un modelo, y un output parser en una sola expresion. Todos los componentes que implementan la interfaz `Runnable` son compatibles con LCEL.

```python
chain = prompt | model | output_parser
result = chain.invoke({"input": "hola"})
```

### Runnable
Interfaz base de LangChain. Cualquier componente que implemente `invoke`, `stream`, y `batch` es un `Runnable` y puede participar en cadenas LCEL o ser usado de forma standalone.

### Middleware
Capa de intercepcion que se ejecuta antes o despues de llamadas al modelo dentro de un agente. Permite modificar el request (ej. cambiar el modelo dinamicamente), agregar logging, validar outputs, y controlar el flujo de ejecucion.

### Parallel tool calls
Capacidad de algunos modelos de solicitar la ejecucion de multiples tools simultaneamente en una sola respuesta. El modelo determina cuando las operaciones son independientes y pueden ejecutarse en paralelo. Se puede desactivar con `parallel_tool_calls=False`.

### Model profile
Diccionario de capacidades y caracteristicas de un modelo especifico: soporte para tool calling, structured output, multimodalidad, tamaño de context window, etc. LangChain lo usa internamente para elegir estrategias optimas (ej. que tipo de structured output usar).

---

## Observabilidad

### LangSmith
Plataforma de observabilidad de LangChain para tracing, evaluacion y monitoreo de aplicaciones LLM. Registra cada llamada al modelo, cada tool call, latencias y costos. Indispensable para debuggear cadenas y agentes complejos.

### Trace
Registro completo de la ejecucion de una cadena o agente: todos los pasos, inputs, outputs, tiempos y costos. En LangSmith cada invocacion genera un trace que puede inspeccionarse en el UI.

---

## Terminos adicionales de LLMs

### Fine-tuning
Proceso de continuar el entrenamiento de un modelo pre-entrenado sobre un dataset especifico para especializarlo en una tarea o dominio. Mas costoso que RAG pero puede producir comportamiento mas consistente en dominios muy especificos.

### Zero-shot
Capacidad de un modelo de realizar una tarea sin ejemplos previos en el prompt. Solo con instrucciones.

### Few-shot
Tecnica de prompting donde se incluyen ejemplos concretos de input/output en el prompt para guiar al modelo hacia el formato o comportamiento esperado.

### Chain of thought (CoT)
Tecnica de prompting que le pide al modelo que razone paso a paso antes de dar una respuesta final. Mejora significativamente el rendimiento en tareas de razonamiento logico y matematica.

### ReAct
Patron de agente que combina razonamiento (Reasoning) y accion (Acting) en un loop: el modelo piensa, actua (llama una tool), observa el resultado, y repite hasta concluir. Es la base de la mayoria de implementaciones de agentes.