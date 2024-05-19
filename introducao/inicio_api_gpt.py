import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

mensagem = "Olá GPT, tudo bem?"

response = client.chat.completions.create(
    model="gpt-3.5-turbo", # motor de IA
    messages=[{'role': 'user', 'content': mensagem}], # mensagem de entrada
    max_tokens=100, # quantidade máxima de tokens na resposta
    temperature=0.5, # quanto mais próximo de 0, mais conservador é o texto gerado
)

# print(response) # mostra o conteúdo completo
print(response.choices[0].message.content) # mostra apenas a resposta