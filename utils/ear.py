import os
import wave
import pyaudio
import numpy as np
from faster_whisper import WhisperModel

class Ear:
    def __init__(self, model_size="base", device="cpu"):
        print("[Ear] Cargando modelo de transcripcion...")
        self.model = WhisperModel(model_size, device=device, compute_type="int8")
        print("[Ear] Modelo listo.")
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.p = pyaudio.PyAudio()
        self.silence_threshold = self._calibrate()

    def _calibrate(self):
        print("[Ear] Calibrando microfono... (mantente en silencio un momento)")
        stream = self.p.open(format=self.format, channels=self.channels,
                             rate=self.rate, input=True, frames_per_buffer=self.chunk)
        amplitudes = []
        for _ in range(20):
            data = stream.read(self.chunk)
            audio_data = np.frombuffer(data, dtype=np.int16)
            amplitudes.append(np.abs(audio_data).mean())
        stream.stop_stream()
        stream.close()
        noise_floor = np.mean(amplitudes)
        threshold = max(noise_floor * 3.5, 300)
        print(f"[Ear] Calibrado. Ruido base: {noise_floor:.0f} | Umbral de activacion: {threshold:.0f}")
        return threshold

    def listen(self, silence_duration=1.5, max_wait=10):
        stream = self.p.open(format=self.format, channels=self.channels,
                             rate=self.rate, input=True, frames_per_buffer=self.chunk)

        print(">>> Escuchando (habla ahora)...")
        frames = []
        silent_chunks = 0
        max_silent_chunks = int(silence_duration * self.rate / self.chunk)
        max_wait_chunks = int(max_wait * self.rate / self.chunk)
        started_talking = False

        while True:
            data = stream.read(self.chunk)
            frames.append(data)
            amplitude = np.abs(np.frombuffer(data, dtype=np.int16)).mean()

            if amplitude > self.silence_threshold:
                if not started_talking:
                    print(">>> Voz detectada...")
                silent_chunks = 0
                started_talking = True
            else:
                if started_talking:
                    silent_chunks += 1

            if started_talking and silent_chunks > max_silent_chunks:
                break

            if not started_talking and len(frames) > max_wait_chunks:
                print(">>> Tiempo de espera agotado, no se detecto voz.")
                stream.stop_stream()
                stream.close()
                return ""

        print(">>> Transcribiendo...")
        stream.stop_stream()
        stream.close()

        temp_file = "temp_audio.wav"
        wf = wave.open(temp_file, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        segments, _ = self.model.transcribe(temp_file, beam_size=5, language="es")
        text = "".join([segment.text for segment in segments]).strip()
        os.remove(temp_file)
        print(f">>> Transcripcion: {text}")
        return text

    def _check_keyword(self, frames, keywords):
        if not frames: return False
        temp_file = "temp_wake.wav"
        try:
            wf = wave.open(temp_file, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            segments, _ = self.model.transcribe(temp_file, beam_size=1, language="es")
            text = "".join([s.text for s in segments]).lower()
            os.remove(temp_file)
            if text.strip():
                print(f"[Ear] Escuchado: '{text.strip()}'")
            return any(kw in text for kw in keywords)
        except:
            return False

    def wait_for_wake_word(self, keywords=None):
        if keywords is None:
            keywords = ["jarvis", "harvis", "yarvis", "garvis", "arvis"]
        
        stream = self.p.open(format=self.format, channels=self.channels,
                             rate=self.rate, input=True, frames_per_buffer=self.chunk)
        
        print(f"[Jarvis] Esperando palabra clave...")
        
        frames_buffer = []
        check_every = int(self.rate / self.chunk * 1.5)

        while True:
            data = stream.read(self.chunk)
            frames_buffer.append(data)
            if len(frames_buffer) > check_every * 2:
                frames_buffer.pop(0)

            # Deteccion de palabra clave cada medio ciclo de ventana
            if len(frames_buffer) >= check_every and len(frames_buffer) % (check_every // 2) == 0:
                if self._check_keyword(frames_buffer, keywords):
                    print("[Jarvis] ¡Palabra detectada!")
                    stream.stop_stream()
                    stream.close()
                    return "keyword"

_ear_instance = None

def listen():
    global _ear_instance
    if _ear_instance is None:
        _ear_instance = Ear(model_size="base")
    return _ear_instance.listen()

def wake_word(keywords=None):
    global _ear_instance
    if _ear_instance is None:
        _ear_instance = Ear(model_size="base")
    return _ear_instance.wait_for_wake_word(keywords=keywords)
