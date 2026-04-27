# Modelos en LangChain: `init_chat_model` vs clases específicas

## Contexto

LangChain ofrece dos formas de inicializar un modelo de lenguaje. La primera es instanciar directamente la clase del proveedor (`ChatOpenAI`, `ChatAnthropic`, etc.). La segunda es usar `init_chat_model`, una función factory que abstrae el proveedor. Ambas producen un objeto con la misma interfaz (`invoke`, `stream`, `batch`, `bind_tools`), pero difieren en flexibilidad, control y casos de uso.

---

## Clases específicas del proveedor

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatOpenAI(model="gpt-4o", temperature=0.7)
model = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=1000)
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
```

Cada clase pertenece a su paquete de integración (`langchain_openai`, `langchain_anthropic`, etc.) y expone los parámetros propios de ese proveedor. Al instanciarlas, el proveedor y el modelo quedan fijos para toda la vida del objeto.

### Parametros destacados

| Parametro | Descripcion |
|---|---|
| `model` | Nombre exacto del modelo segun el proveedor |
| `temperature` | Aleatoriedad de la respuesta (0 = determinista) |
| `max_tokens` | Limite de tokens en la respuesta |
| `api_key` | Clave de autenticacion (o via variable de entorno) |
| `timeout` | Tiempo maximo de espera en segundos |
| `max_retries` | Reintentos ante errores de red o rate limit (default: 6) |

Ademas de estos estandares, cada clase puede tener parametros propios. Por ejemplo, `ChatOpenAI` tiene `use_responses_api` para elegir entre la API de Responses o Completions. Esos parametros no existen en otras clases ni en `init_chat_model`.

### Cuando usarlas

- El proveedor esta definido desde el inicio y no va a cambiar.
- Necesitas parametros exclusivos del SDK de ese proveedor.
- Quieres que el codigo sea explicito sobre con que modelo estas trabajando.
- Estas en produccion con un proveedor contratado y fijo.

---

## `init_chat_model`

```python
from langchain.chat_models import init_chat_model

# Inferencia automatica del proveedor por nombre de modelo
model = init_chat_model("claude-sonnet-4-6")

# Formato explicito provider:model
model = init_chat_model("openai:gpt-4o")
model = init_chat_model("google_genai:gemini-2.5-flash-lite")

# Con parametros estandar
model = init_chat_model("claude-sonnet-4-6", temperature=0.7, max_tokens=1000)
```

`init_chat_model` es una funcion factory que recibe el nombre del modelo, detecta el proveedor (por el nombre o por el prefijo `provider:model`) e instancia la clase correcta internamente. El objeto resultante tiene exactamente la misma interfaz que las clases directas.

### La diferencia real: modelos configurables en runtime

Si no se especifica modelo al crear la instancia, el modelo queda como campo configurable. Esto permite cambiar de modelo en cada invocacion sin modificar el codigo:

```python
# Sin modelo fijo
configurable_model = init_chat_model(temperature=0)

# Distintos modelos en distintas llamadas
configurable_model.invoke(
    "Explica que es un transformer",
    config={"configurable": {"model": "gpt-4o"}}
)

configurable_model.invoke(
    "Explica que es un transformer",
    config={"configurable": {"model": "claude-sonnet-4-6"}}
)
```

Tambien se puede fijar un modelo por defecto y exponer solo ciertos campos como configurables:

```python
model = init_chat_model(
    "gpt-4o",
    configurable_fields=("model", "model_provider", "temperature", "max_tokens"),
    temperature=0.7,
)

# El llamador puede sobreescribir temperatura o incluso cambiar de modelo
model.invoke(
    "Hola",
    config={"configurable": {"model": "claude-sonnet-4-6", "temperature": 0}}
)
```

Los modelos configurables son compatibles con `bind_tools`, `with_structured_output` y el encadenamiento de LCEL, igual que cualquier otro modelo.

### Cuando usarlo

- Quieres cambiar de proveedor o modelo sin tocar el codigo de la aplicacion.
- Estas construyendo una app donde el usuario elige el modelo.
- Estas en la fase de experimentacion y vas a comparar varios modelos.
- Construyes una libreria o herramienta generica que no debe depender de un proveedor especifico.
- Usas LangGraph y quieres que el modelo sea un parametro configurable del grafo.

---

## Comparacion directa

| Aspecto | Clases directas | `init_chat_model` |
|---|---|---|
| Proveedor | Fijo en el codigo | Intercambiable |
| Parametros exclusivos del SDK | Acceso total | Solo parametros estandar |
| Cambiar modelo en runtime | No es posible | Si, via `config` |
| Verbosidad del codigo | Explicito, mas imports | Compacto, un solo import |
| Inferencia automatica del proveedor | No aplica | Si, por nombre de modelo |
| Compatibilidad con LCEL / LangGraph | Total | Total |
| Recomendado para produccion con proveedor fijo | Si | Tambien funciona |

---

## Convivencia de ambos enfoques

No son mutuamente excluyentes. Un patron comun es usar `init_chat_model` como interfaz principal y recurrir a la clase directa solo cuando se necesita un parametro especifico del proveedor:

```python
# Caso general con init_chat_model
agent_model = init_chat_model("openai:gpt-4o", temperature=0)

# Caso especifico donde se necesita un param exclusivo de OpenAI
from langchain_openai import ChatOpenAI
responses_model = ChatOpenAI(model="gpt-4o", use_responses_api=True)
```

---

## Instalacion

Cada proveedor requiere su paquete de integracion, independientemente de cual de los dos enfoques uses:

```bash
pip install langchain[openai]       # OpenAI
pip install langchain[anthropic]    # Anthropic
pip install langchain[google-genai] # Google Gemini
pip install langchain[aws]          # AWS Bedrock
pip install langchain[huggingface]  # HuggingFace
```

`init_chat_model` importa el paquete del proveedor en tiempo de ejecucion, por lo que igual necesitas tenerlo instalado.