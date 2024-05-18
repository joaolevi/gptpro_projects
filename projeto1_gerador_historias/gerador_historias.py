from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# prompt = (
#     "Você é um escritor famoso com vários livros best-seller\n" # Role
#     "Sua tarefa é escrever uma história baseada na [CARACTERISTICA_1], [CARACTERISTICA_1], [CARACTERISTICA_1] e [CARACTERISTICA_1].\n" # Context
#     # Task
# )

prompt = (
    "Você é um escritor famoso com vários livros best-seller\n" # Role
    "Sua tarefa é escrever uma história baseada na QUANTIDADE_DE_PERSONAGENS, ERA, LUGAR e GÊNERO.\n" # Context
    # Task
)

caracteristicas = {
    "QUANTIDADE_DE_PERSONAGENS": "4",
    "ERA": "medieval",
    "LUGAR": "castelo",
    "GÊNERO": "aventura",
}

def gerar_historia(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{'role': 'system', 'content': prompt+" ".join([f"{k}: {v}\n" for k, v in caracteristicas.items()])}],
        max_tokens=1000,
        temperature=0.5,
    )
    return response.choices[0].message.content

# texto = gerar_historia(prompt)
# print(texto)

# # salvar o texto em um .txt
# with open("historia.txt", "w") as f:
#     f.write(texto)

prompt2 = (
    """Você é um head de produto focado na história do usuário.
    Sua tarefa é gerar 3 textos que descrevam cenários de uso para um produto de software 
    considerando o TIPO_DO_SOFTWARE, FAIXA_ETARIA_USUARIOS, PLATAFORMA.
    Cada usuário deve ter nome e sobrenome, e o cenário deve ser descrito em 3 parágrafos, utilize markdown para formatar o texto. 
    """ # Context
    # Task
)

caracteristicas2 = {
    "TIPO_DO_SOFTWARE": "aplicativo de delivery",
    "FAIXA_ETARIA_USUARIOS": "18-35",
    "PLATAFORMA": "iOS",
}

def gerar_historia2(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{'role': 'system', 'content': prompt+" ".join([f"{k}: {v}\n" for k, v in caracteristicas2.items()])}],
        max_tokens=1000,
        temperature=0.5,
    )
    return response.choices[0].message.content

texto2 = gerar_historia2(prompt2)

# salvar o texto em um .txt
with open("historia2.txt", "w") as f:
    f.write(texto2)

