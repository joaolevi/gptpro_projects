from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

prompt = [
    {"role": "system", "content": "Você é um escritor famoso com vários livros best-seller"},
    {"role": "user", "content": "Sua tarefa é escrever uma história baseada na [CARACTERISTICA_1], [CARACTERISTICA_2], [CARACTERISTICA_3] e [CARACTERISTICA_4]."},
]

caracteristicas = {
    "QUANTIDADE_DE_PERSONAGENS": "4",
    "ERA": "medieval",
    "LUGAR": "castelo",
    "GÊNERO": "aventura",
}

prompt.append({"role": "user", "content": " ".join([f"{k}: {v}\n" for k, v in caracteristicas.items()])})

print(prompt)

def gerar_historia(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=1000,
        temperature=0.5,
    )
    return response.choices[0].message.content

texto = gerar_historia(prompt)
print(texto)

# # salvar o texto em um .txt
# with open("historia.txt", "w") as f:
#     f.write(texto)
