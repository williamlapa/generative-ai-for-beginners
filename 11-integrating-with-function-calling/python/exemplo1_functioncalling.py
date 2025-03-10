import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
client = OpenAI()

deployment = "gpt-3.5-turbo"

# Criando uma mensagem de usuário
messages = [{"role": "user", "content": "Find me a good course for a beginner student to learn Azure."}]

# Definição da função que será chamada pelo modelo
functions = [
   {
      "name": "search_courses",
      "description": "Retrieves courses from the search index based on the parameters provided",
      "parameters": {
         "type": "object",
         "properties": {
            "role": {
               "type": "string",
               "description": "The role of the learner (i.e. developer, data scientist, student, etc.)"
            },
            "product": {
               "type": "string",
               "description": "The product that the lesson is covering (i.e. Azure, Power BI, etc.)"
            },
            "level": {
               "type": "string",
               "description": "The level of experience the learner has prior to taking the course (i.e. beginner, intermediate, advanced)"
            }
         },
         "required": ["role"]
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

# Definição da função para buscar cursos na API da Microsoft Learn
def search_courses(role, product, level):
    url = "https://learn.microsoft.com/api/catalog/"
    params = {
        "role": role,
        "product": product,
        "level": level
    }
    response = requests.get(url, params=params)
    modules = response.json()["modules"]
    
    results = [{"title": module["title"], "url": module["url"]} for module in modules[:5]]
    
    return str(results)

# Verificando se o modelo quer chamar uma função
if response_message.function_call.name:
    function_name = response_message.function_call.name

    available_functions = {
        "search_courses": search_courses,
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

print("Final response:")
print("*" * 50)
print(second_response.choices[0].message)
