import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()
client = OpenAI()

token_brapi= "gYm8yaq8YkjuFbPuEk5rWs"

deployment = "gpt-3.5-turbo"

# Criando uma mensagem de usuário
messages = [{"role": "user", "content": "Qual é a cotação atual da ação PETR4?"}]

# Definição da função que será chamada pelo modelo
functions = [
   {
      "name": "get_stock_price",
      "description": "Obtém a cotação atual de uma ação nos mercados financeiros.",
      "parameters": {
         "type": "object",
         "properties": {
            "stock_symbol": {
               "type": "string",
               "description": "O código da ação (exemplo: AAPL para Apple, PETR4 para Petrobras)."
            },
            "market": {
               "type": "string",
               "description": "O mercado onde a ação é negociada (exemplo: US para Estados Unidos, BR para Brasil)."
            }
         },
         "required": ["stock_symbol", "market"]
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

# Definição da função para buscar a cotação da ação e a data/hora
def get_stock_price(stock_symbol, market):
    if market == "US":
        url = f"https://financialmodelingprep.com/api/v3/quote/{stock_symbol}?apikey=demo"
    elif market == "BR":
        url = f"https://brapi.dev/api/quote/{stock_symbol}"
    else:
        return "Mercado não suportado"
    
    response = requests.get(url)
    data = response.json()
    
    if market == "US":
        if isinstance(data, list) and len(data) > 0:
            price = data[0].get("price", "Preço não encontrado")
            last_updated = datetime.utcfromtimestamp(data[0].get("timestamp", 0)).strftime('%Y-%m-%d %H:%M:%S UTC')
        else:
            return "Erro ao obter dados da ação nos EUA"
    elif market == "BR":
        if "results" in data and len(data["results"]) > 0:
            price = data["results"][0].get("regularMarketPrice", "Preço não encontrado")
            last_updated = data["results"][0].get("regularMarketTime", "Data não encontrada")
        else:
            return "Erro ao obter dados da ação no Brasil"
    
    return f"Ação {stock_symbol} ({market}): {price} (Última atualização: {last_updated})"

# Verificando se o modelo quer chamar uma função
if response_message.function_call.name:
    function_name = response_message.function_call.name

    available_functions = {
        "get_stock_price": get_stock_price,
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
