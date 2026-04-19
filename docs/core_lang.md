# Conceptos Fundamentales de LangChain (El "Core")

LangChain está diseñado en torno a una serie de abstracciones principales. Conocer estas abstracciones es el primer paso para dominar el desarrollo con Modelos de Lenguaje.

## 1. Modelos de Lenguaje (LLMs / ChatModels)
Son el corazón de cualquier aplicación con IA. LangChain proporciona una interfaz estandarizada para interactuar con diferentes proveedores (OpenAI, Anthropic, Google, etc.).
*   **ChatModels:** Son la interfaz más moderna y recomendada. Reciben una lista de "Mensajes" y devuelven un "Mensaje". Están optimizados para el diálogo.
*   **Inicialización:** LangChain permite inicializar modelos de forma estándar usando `init_chat_model()`, lo cual facilita cambiar de un proveedor a otro.

## 2. Mensajes (Messages)
Para comunicarnos con los `ChatModels`, usamos objetos de tipo Mensaje. Hay diferentes roles:
*   **`SystemMessage`:** Da las instrucciones generales de comportamiento al modelo (ej. "Eres un asistente útil que habla en español").
*   **`HumanMessage`:** Representa la entrada del usuario.
*   **`AIMessage`:** Representa la respuesta del modelo de IA.
*   **`ToolMessage`:** Contiene el resultado de la ejecución de una herramienta.

## 3. Plantillas de Prompts (Prompt Templates)
En lugar de codificar textos largos (hardcoding), usamos plantillas dinámicas. Te permiten insertar variables antes de enviar el texto al modelo.
*   **`ChatPromptTemplate`:** Es la clase principal. Permite estructurar una secuencia de mensajes (Sistema, Usuario) y pasarles variables dinámicamente usando llaves `{variable}`.

## 4. Analizadores de Salida (Output Parsers)
Los LLMs siempre devuelven texto (strings). Si necesitas que tu programa en Python trabaje con listas, diccionarios o objetos específicos, necesitas un analizador.
*   Permiten convertir la respuesta de texto plano del modelo en datos estructurados (como JSON).
*   **Structured Output (Salida Estructurada):** La forma más moderna, combinando **Pydantic** para forzar al LLM a devolver siempre la estructura de datos requerida.
*   **Custom Parsers (`BaseTransformOutputParser`):** LangChain permite crear tus propios limpiadores/transformadores de texto heredando de esta clase. Al conectarlo al modelo (`modelo | mi_parser`), intercepta el objeto complejo `AIMessage`, extrae el texto puro (`.content`), le aplica tu lógica personalizada (ej. limpiar Markdown) y te devuelve un `str` listo para usar, soportando *streaming* de forma automática.

## 5. LCEL (LangChain Expression Language) y Runnables
LCEL es una sintaxis especial que usa el símbolo `|` (pipe) para encadenar componentes de forma intuitiva. Todo en LCEL se basa en la interfaz **`Runnable`**.
```python
cadena = prompt | modelo | parser
resultado = cadena.invoke({"tema": "LangChain"})
```
*   **Métodos clave de un Runnable:** Todos los objetos core comparten métodos como `.invoke()` (ejecutar una vez), `.stream()` (devolver por fragmentos), y `.batch()` (ejecutar múltiples entradas). También sus versiones asíncronas (`.ainvoke()`, etc.).
*   **`RunnablePassthrough` y `RunnableParallel`:** Clases útiles para pasar datos sin modificar o ejecutar varias tareas al mismo tiempo dentro de la cadena.

## 6. Documentos (Documents)
Cuando trabajas con RAG (Retrieval-Augmented Generation) para leer PDFs o webs, el texto no flota libremente, sino que se encapsula en la clase `Document`.
*   Un `Document` tiene dos atributos principales: `page_content` (el texto en sí) y `metadata` (un diccionario con información como el autor, la página, la URL, etc.).

## 7. Herramientas (Tools)
Son funciones que el LLM puede decidir ejecutar (como buscar en internet o consultar una base de datos).
*   **Decorador `@tool`:** Es la forma más fácil de convertir una función normal de Python en una herramienta que LangChain entienda, usando los *docstrings* y los tipos de datos (type hints) de Python para explicarle al LLM qué hace la función.

---

## Librerías y Paquetes Útiles del Ecosistema

Además del `langchain-core`, estas son las librerías imprescindibles en el día a día:

1.  **Integraciones Oficiales:**
    *   `langchain-openai`: Métodos específicos para ChatGPT y Embeddings de OpenAI.
    *   `langchain-anthropic`: Para los modelos Claude.
    *   `langchain-google-genai`: Para modelos Gemini.
2.  **`langchain-community`:**
    *   Una librería masiva mantenida por la comunidad que tiene literalmente miles de conectores (Document Loaders para leer Notion, Slack, conectores a bases de datos raras, etc.). Si necesitas conectar una herramienta externa, búscalo aquí primero.
3.  **`langsmith`:**
    *   El SDK para conectar tu código a la plataforma LangSmith. Útil para "trazabilidad" (tracing). Al poner la variable de entorno `LANGCHAIN_TRACING_V2=true`, podrás ver en una interfaz web exactamente qué prompts se enviaron, cuánto tardó cada paso y cuántos tokens se gastaron.
4.  **`python-dotenv`:**
    *   No es exclusiva de LangChain, pero es obligatoria. Sirve para cargar tu archivo `.env` de forma segura mediante `load_dotenv()`, protegiendo así tus API Keys.
