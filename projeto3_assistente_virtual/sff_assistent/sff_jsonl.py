import csv
import json

input_csv_file = 'projeto3_assistente_virtual/dados/ssf_dataset.csv'
output_jsonl_file = 'projeto3_assistente_virtual/dados/ssf_prompt.jsonl'

with open(input_csv_file, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with open(output_jsonl_file, mode='w', encoding='utf-8') as jsonl_file:
        for row in csv_reader:
            mensagem_cliente = {"role": "user", "content": row['cliente']}
            resposta_assistente = {"role": "assistant", "content": row['assistente']}
    
            jsonl_file.write(json.dumps(mensagem_cliente) + '\n')
            jsonl_file.write(json.dumps(resposta_assistente) + '\n')

print(f"Jsonl criado com sucesso: {output_jsonl_file}")