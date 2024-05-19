from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

PATH = "projeto4_aprendizado_idiomas/speech_to_text/"

def transcribe_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            response_format="text")
    return transcript

audio_file_path = PATH+"audios/audio1.ogg"
transcription = transcribe_audio(audio_file_path)

print("Transcrição:", transcription)

with open(PATH+"transcricoes/texto_transcrito.txt", "w", encoding="utf-8") as txt_file:
    txt_file.write(transcription)
