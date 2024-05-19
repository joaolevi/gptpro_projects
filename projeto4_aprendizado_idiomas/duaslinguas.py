from openai import OpenAI
import gradio as gr
import whisper
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
model = whisper.load_model("base")


def transcribe(file):
    options = whisper.DecodingOptions(language="pt")
    result = model.transcribe(file, options=options)
    
    options = whisper.DecodingOptions()
    result = whisper.decode(model, options)
    return result.text

prompts = {
    'START': 'Classifique a intenção da próxima entrada. É: ENSINAR_IDIOMA, INDICAR_IDIOMA, PERGUNTA_DE_IDIOMA, SOLICITAR_FRASE, OUTRO? Responda com apenas uma palavra.',
    'ENSINAR_IDIOMA': 'Se o usuário disser que quer aprender um idioma: PERGUNTAR_QUAL_IDIOMA, se não estiver claro: MAIS, se não puder ensinar: OUTRO. Responda com apenas uma palavra..',
    'PERGUNTAR_QUAL_IDIOMA': 'Agora pergunte ao usuário qual idioma ele quer aprender.',
    'INDICAR_IDIOMA': 'Se o usuário indicou o idioma: FORNECER_FRASE, se não estiver claro: MAIS, se não puder indicar: OUTRO. Responda com apenas uma palavra..',
    'PERGUNTA_DE_IDIOMA': 'Se você puder responder à pergunta de idioma: RESPONDER, se precisar de mais informações: MAIS, se não puder responder: OUTRO. Responda com apenas uma palavra..',
    'SOLICITAR_FRASE': 'Se o usuário solicitou uma frase de prática: PERGUNTAR_QUAL_IDIOMA, se não estiver claro: MAIS, se não puder fornecer: OUTRO. Responda com apenas uma palavra..',
    'FORNECER_FRASE': 'Agora forneça uma frase para prática de aprendizado de idiomas e PEDIR_AUDIO.',
    'RESPONDER': 'Agora responda à pergunta de idioma como um assistente educado.',
    'CORRIGIR': 'Se o usuario disser a frase fornecida no audio: FEEDBACK_AUDIO, se não estiver claro: MAIS, se não puder corrigir: OUTRO. Responda com apenas uma palavra..',
    'MAIS': 'Agora peça mais informações como um assistente de aprendizado de idiomas educado.',
    'OUTRO': 'Agora diga que você não pode responder à pergunta ou fornecer feedback como um assistente de aprendizado de idiomas educado.',
    'PEDIR_AUDIO': 'Por favor, envie o áudio falando a frase fornecida para análise.',
    'FEEDBACK_AUDIO': 'Agora forneça feedback sobre o seguinte áudio: "{audio}"'
}

actions = {
    'ACAO_CORRIGIR_AUDIO': 'O feedback sobre o áudio foi fornecido. Agora diga que a ação foi concluída em linguagem natural.',
    'ACAO_FORNECER_FRASE_ADICIONAL': 'Uma frase adicional foi fornecida para prática. Agora diga que a ação foi concluída em linguagem natural.',
    'ACAO_RESPONDER_PERGUNTA': 'A pergunta de idioma foi respondida. Agora diga que a ação foi concluída em linguagem natural.',
    'ACAO_PEDIR_MAIS_INFORMACOES': 'Mais informações foram solicitadas. Agora diga que a ação foi concluída em linguagem natural.',
    'ACAO_NAO_PODER_RESPONDER': 'Informar que a pergunta ou solicitação não pode ser respondida. Agora diga que a ação foi concluída em linguagem natural.'
}

messages = [
    {"role": "user", "content": prompts['START']},
]

def generate_answer(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages)
    return (response.choices[0].message.content)


def start(user_input):
    messages.append({"role": "user", "content": user_input})
    return discussion(messages, 'START')


def discussion(messages, last_step):
    answer = generate_answer(messages)
    print(answer)
    if answer in prompts.keys():
        messages.append({"role": "assistant", "content": answer})
        messages.append({"role": "user", "content": prompts[answer]})
        return discussion(messages, answer)
    elif answer.split("|")[0].strip() in actions.keys():
        return do_action(answer)
    else:
        if last_step != 'MORE':
            messages = []
        last_step = 'END'
        return answer


def do_action(answer):
    print("Doing action " + answer)
    messages.append({"role": "assistant", "content": answer})
    action = answer.split("|")[0].strip()
    messages.append({"role": "user", "content": actions[action]})
    return discussion(messages, answer)


def start_chat(file):
    input = transcribe(file)
    print(input)
    return start(input)


gr.Interface(
    theme=gr.themes.Soft(),
    fn=start_chat,
    live=True,
    inputs=gr.Audio(sources="microphone", type="filepath"),
    outputs="text").launch()