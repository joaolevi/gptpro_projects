from openai import OpenAI
import gradio as gr
import whisper
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
model = whisper.load_model("base")


def transcribe(file):
    print(file)
    transcription = model.transcribe(file)
    return transcription['text']

def gerador_respostas(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0.7)
    return (response.choices[0].message.content)

prompts = {
    'INICIO': 'Classifique a intenção da próxima entrada. É: PERGUNTA_DE_IDIOMA, OUTRO? Responda com apenas uma palavra.',
    'PERGUNTA_DE_IDIOMA': 'Se for uma pergunta sobre um idioma: RESPONDER, se precisar de mais informações: MAIS, se não puder responder: OUTRO. Responda com apenas uma palavra.',
    'RESPONDER': 'Agora responda à pergunta de idioma como um assistente educado.',
    'MAIS': 'Agora peça mais informações como um assistente de aprendizado de idiomas educado.',
    'OUTRO': 'Diga que você não pode responder à pergunta e peça para o usuário tentar novamente.',
}

messages = [
    {"role": "user", "content": prompts['INICIO']},
]

def conversa(messages, last_step):
    answer = gerador_respostas(messages)
    if answer == 'OUTRO':
        return 'Desculpe, não posso responder a essa pergunta. Por favor, tente novamente.'
    print(answer)
    if answer in prompts.keys():
        messages.append({"role": "assistant", "content": answer})
        messages.append({"role": "user", "content": prompts[answer]})
        return conversa(messages, answer)
    else:
        if last_step != 'MAIS':
            messages = []
        last_step = 'FIM'
        return answer

def start_chat(file):
    input = transcribe(file)
    print(input)
    messages.append({"role": "user", "content": input})
    return conversa(messages, 'INICIO')


gr.Interface(
    theme=gr.themes.Soft(),
    fn=start_chat,
    live=True,
    inputs=gr.Audio(sources="microphone", type="filepath"),
    outputs="text").launch()