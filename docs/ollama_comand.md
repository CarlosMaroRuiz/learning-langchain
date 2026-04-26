# Comandos Esenciales de Ollama

Esta es una guía rápida de los comandos más utilizados para gestionar tus modelos locales.

## Gestión de Modelos
| Comando | Descripción |
| :--- | :--- |
| `ollama run <modelo>` | Descarga (si no existe) y ejecuta un modelo en modo chat. |
| `ollama list` | Lista todos los modelos descargados en tu máquina. |
| `ollama pull <modelo>` | Descarga un modelo del registro sin ejecutarlo. |
| `ollama rm <modelo>` | Elimina un modelo de tu almacenamiento local. |
| `ollama cp <modelo> <nuevo_nombre>` | Crea una copia de un modelo con un nuevo nombre. |

## Estado del Sistema
| Comando | Descripción |
| :--- | :--- |
| `ollama ps` | Muestra qué modelos están cargados actualmente en la memoria RAM. |
| `ollama serve` | Inicia el servidor de Ollama (útil si no está corriendo como servicio). |

## Comandos dentro del Chat (`ollama run`)
Una vez dentro de una sesión de chat, puedes usar estos comandos precedidos por una diagonal `/`:

*   `/bye`: Sale de la sesión de chat actual.
*   `/list`: Lista los modelos disponibles.
*   `/show info`: Muestra información técnica del modelo cargado.
*   `/set parameter <parámetro> <valor>`: Ajusta parámetros como `temperature` o `num_ctx`.
*   `/help`: Muestra la ayuda completa de comandos internos.

---
> **Tip:** Puedes ver la lista completa de modelos disponibles para descargar en [ollama.com/library](https://ollama.com/library).
