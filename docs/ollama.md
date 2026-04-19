# Ollama y LangChain: Guía de Integración Local

## 1. ¿Qué es Ollama?
Ollama es un motor de software que te permite descargar y ejecutar Modelos de Lenguaje Grandes (LLMs) como *Llama 3, DeepSeek, Qwen o Mistral* de forma 100% local en tu propia computadora. Actúa como un servidor local (por defecto en `http://localhost:11434`) al cual LangChain puede hacerle peticiones tal y como si le hablara a la API de OpenAI, pero sin internet y sin pagar por tokens.

## 2. Instalación y Ejecución de Modelos
1. **Instalar el Software:** Descarga el ejecutable desde [ollama.com](https://ollama.com/) e instálalo en tu sistema operativo.
2. **Descargar y Ejecutar un Modelo:** Abre cualquier terminal (CMD, PowerShell, Bash) y ejecuta el comando con el nombre del modelo que quieres usar. Por ejemplo:
   ```bash
   ollama run deepseek-r1:1.5b
   ```
   *Nota: La primera vez que corras esto, Ollama descargará los "pesos" del modelo (puede tardar dependiendo de tu internet). Una vez descargado, el modelo quedará activo en la memoria de tu PC.*

## 3. Configuración en LangChain
Para conectar tu código de LangChain con tu modelo local de Ollama, debes usar el paquete oficial.

**Paso A: Instalar el paquete**
Abre la terminal de tu proyecto y ejecuta:
```bash
uv pip install langchain-ollama
```

**Paso B: Código de uso (Sintaxis LCEL)**
Como `ChatOllama` cumple con la interfaz universal `Runnable`, reemplazar tu modelo de la nube por el local es tan sencillo como cambiar un par de líneas de código.

```python
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Instanciar el modelo local
llm_local = ChatOllama(
    model="deepseek-r1:1.5b",  # Debe coincidir exactamente con el que bajaste
    temperature=0.7
)

# 2. Uso con memoria y cadenas (Igual que con ChatOpenAI)
chat_history = [
    SystemMessage(content="Eres un asistente muy inteligente que corre localmente.")
]
chat_history.append(HumanMessage(content="¿Cómo te llamas?"))

# Ejecución en streaming
for chunk in llm_local.stream(chat_history):
    print(chunk.content, end="", flush=True)
```

## 4. ¿Por qué usar Ollama (Pros y Contras)?
### Ventajas (Pros)
*   **Privacidad Absoluta:** Ningún dato, prompt o conversación tuya sale hacia internet. Fundamental para datos empresariales sensibles.
*   **Gratis Ilimitado:** No hay "costo por token". Puedes chatear 24/7 sin gastar un centavo.
*   **Ideal para RAG:** Puedes pasarle miles de PDFs y gigabytes de texto para que los lea sin miedo a una factura sorpresa.

### Desventajas (Contras)
*   **Límite de Hardware:** La inteligencia del modelo dependerá de la Memoria RAM de tu PC y de tu Tarjeta Gráfica (GPU). 
*   **Modelos más pequeños:** Los modelos gigantes de la nube (como GPT-4o o Claude 3.5 Sonnet) corren en supercomputadoras que cuestan millones de dólares. Tu PC solo podrá correr modelos "destilados" o de menos parámetros (1.5B, 8B, 14B), los cuales son muy buenos, pero no alcanzan el intelecto top de los modelos cerrados gigantes.
