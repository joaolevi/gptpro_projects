from openai import OpenAI
from dotenv import load_dotenv
import os
import jsonlines

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

prompt = [{"role": "system", "content": """Você é um assistente virtual da empresa SuperFastFood que oferece suporte ao cliente.
           Seu telefone para contato é (11) 4001-4002 e o email é "contato@sff.com.br"
           Responda às perguntas dos clientes de forma clara e amigável"""}]

jsonl = jsonlines.open("projeto3_assistente_virtual/dados/ssf_prompt.jsonl")

prompt += jsonl

print(prompt)

def get_response(question):
    full_prompt = prompt + [{"role": "user", "content": question}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=full_prompt,
        max_tokens=100,
        temperature=0.7
    )
    answer = response.choices[0].message.content
    return answer
