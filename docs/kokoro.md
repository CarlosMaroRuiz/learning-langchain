# Kokoro TTS

Kokoro es un modelo de generacion de voz (Text-to-Speech) de codigo abierto diseñado para ser extremadamente ligero y rapido, manteniendo una calidad de audio muy alta y natural.

## Caracteristicas principales
1. Eficiencia: Tiene solo 82 millones de parametros, lo que permite que se ejecute en casi cualquier hardware moderno sin necesidad de grandes servidores.
2. Calidad: A pesar de su tamaño reducido, ofrece una prosodia y naturalidad superior a muchos modelos mas grandes.
3. ONNX Runtime: La version ONNX permite una ejecucion optimizada tanto en CPU como en GPU utilizando tecnologias como DirectML (para tarjetas AMD) o CUDA (para NVIDIA).


## Dependencias necesarias
Para utilizarlo en Python con aceleracion por hardware en Windows, se requieren:
- kokoro-onnx
- onnxruntime-directml
- sounddevice
- numpy

## Archivos requeridos
El modelo requiere dos archivos externos para funcionar:
1. El archivo del modelo (ejemplo: kokoro-v1.0.onnx)
2. El archivo de voces (ejemplo: voices-v1.0.bin)
