from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

prompt = ([
    {"role": "system", "content": "Você é um assistente virtual para suporte ao cliente. Responda às perguntas dos clientes de forma clara e amigável."},
    {"role": "user", "content": "Como posso rastrear meu pedido?"},
    {"role": "assistant", "content": "Você pode rastrear seu pedido acessando a seção 'Meus Pedidos' no nosso site e inserindo seu número de rastreamento."},
    {"role": "user", "content": "Qual é a política de devolução?"},
    {"role": "assistant", "content": "Nossa política de devolução permite devoluções dentro de 30 dias da compra. Por favor, visite nossa página de devoluções para mais detalhes."},
])

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

# question = "Como posso rastrear meu pedido?"
question = input("Digite sua pergunta: ")
print("Cliente:", question)
print("Assistente:", get_response(question))
