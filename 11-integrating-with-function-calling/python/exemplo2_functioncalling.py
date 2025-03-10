import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()
client = OpenAI()

deployment = "gpt-3.5-turbo"

# Criando uma mensagem de usuário
messages = [{"role": "user", "content": "Qual é a cotação atual do dólar para real?"}]

# Definição da função que será chamada pelo modelo
functions = [
   {
      "name": "get_exchange_rate",
      "description": "Obtém a cotação atual do dólar para real e a data/hora da última atualização.",
      "parameters": {
         "type": "object",
         "properties": {
            "base_currency": {
               "type": "string",
               "description": "A moeda base da cotação (exemplo: USD)."
            },
            "target_currency": {
               "type": "string",
               "description": "A moeda alvo da cotação (exemplo: BRL)."
            }
         },
         "required": ["base_currency", "target_currency"]
      }
   }
]

# Chamada da API do OpenAI
response = client.chat.completions.create(
    model=deployment, 
    messages=messages,
    functions=functions, 
    function_call="auto"
)

response_message = response.choices[0].message
print(response_message)

# Definição da função para buscar a cotação do dólar e a data/hora

def get_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    
    exchange_rate = data["rates"].get(target_currency, "Taxa não encontrada")
    last_updated = datetime.utcfromtimestamp(data["time_last_updated"]).strftime('%Y-%m-%d %H:%M:%S UTC')
    
    return f"1 {base_currency} = {exchange_rate} {target_currency} (Última atualização: {last_updated})"

# Verificando se o modelo quer chamar uma função
if response_message.function_call.name:
    function_name = response_message.function_call.name

    available_functions = {
        "get_exchange_rate": get_exchange_rate,
    }
    function_to_call = available_functions[function_name] 

    function_args = json.loads(response_message.function_call.arguments)
    function_response = function_to_call(**function_args)

    messages.append(
        {
            "role": "function",
            "name": function_name,
            "content": function_response,
        }
    )

# Enviando a resposta final ao modelo
second_response = client.chat.completions.create(
    messages=messages,
    model=deployment,
    function_call="auto",
    functions=functions,
    temperature=0
)

print("Resposta Final:")
print("*" * 50)
print(second_response.choices[0].message)

