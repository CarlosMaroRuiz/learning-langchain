from kokoro_onnx import Kokoro
import sounddevice as sd
import os
import threading

class VoiceEngine:
    def __init__(self, model_name="kokoro-v1.0.onnx", voices_name="voices-v1.0.bin"):
        base_path = "kokoro_config"
        model_path = os.path.join(base_path, model_name)
        voices_path = os.path.join(base_path, voices_name)
        
        if not os.path.exists(model_path) or not os.path.exists(voices_path):
            raise FileNotFoundError(f"No se encontraron los archivos de voz en {base_path}")
            
        self.kokoro = Kokoro(model_path, voices_path)
        self.voice = "am_adam"
        self.lang = "es"

    def say(self, text: str, wait=True):
        if not text.strip():
            return

        try:
            samples, sample_rate = self.kokoro.create(
                text, 
                voice=self.voice, 
                speed=1.0, 
                lang=self.lang
            )
            
            sd.play(samples, sample_rate)
            if wait:
                sd.wait()
        except Exception as e:
            print(f"Error en el motor de voz: {e}")

_engine = None

def speak(text: str, wait=True):
    global _engine
    if _engine is None:
        _engine = VoiceEngine()
    
    if not wait:
        threading.Thread(target=_engine.say, args=(text, True), daemon=True).start()
    else:
        _engine.say(text, wait=True)

def voice_pipe(input_data):
    if isinstance(input_data, str):
        speak(input_data, wait=True)
    return input_data
