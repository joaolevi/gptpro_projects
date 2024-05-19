from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

PATH = "projeto4_aprendizado_idiomas/audios/"
def synthesize_speech(text):
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="shimmer",
        input=text,
    ) as response:
        response.stream_to_file(PATH+"resenha4.mp3")

text = "Tem que respeitar o Levi, ele é melhor!"
synthesize_speech(text)
