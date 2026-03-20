import pyttsx3
import threading

class LocalAudioEngine:
    def __init__(self):
        # Initialize pyttsx3 in a thread-safe way
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)  # slightly faster for Jarvis
        # Find a suitable voice
        voices = self.engine.getProperty('voices')
        for voice in voices:
            # Prefer a standard English masculine or neutral robotic voice if possible
            if "david" in voice.name.lower() or "zira" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
    def speak(self, text: str):
        """Play TTS locally without blocking."""
        def run_tts():
            # Initialize a new COM object per thread on Windows/pyttsx3 if needed
            # For simplicity, we lock it with thread execution
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 170)
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"[AudioEngine Error] {e}")

        threading.Thread(target=run_tts, daemon=True).start()

    # Note on STT: Since the client dictates front-end recording,
    # the frontend typically captures audio -> sends as blob via websocket ->
    # Backend local STT transcodes it via faster_whisper or similar.
    def stt_transcribe(self, audio_data) -> str:
        """
        Placeholder for STT.
        Setup instructions for developer:
        1. pip install faster-whisper
        2. Replace this with:
        model = WhisperModel("base.en", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_data)
        return ''.join([s.text for s in segments])
        """
        return ""
