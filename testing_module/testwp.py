import whisper
import os

whisper_model = whisper.load_model("base", download_root=os.path.join(os.getcwd(), "whisper_model"))
result = whisper_model.transcribe(".\Record (online-voice-recorder.com).mp3")