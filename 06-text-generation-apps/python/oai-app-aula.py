from openai import OpenAI
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# configure OpenAI service client 
client = OpenAI()
#deployment = "gpt-3.5-turbo"
deployment = "gpt-4o-mini"

# add your completion code
prompt = """Suggest a beginner lesson for Python in the following format:

        Format:
        - concepts:
        - brief explanation of the lesson:
        - exercise in code with solutions 
        
        Escreve em português do Brasil"""

system = "Você um especialista em linguagem Python"
messages = [{"role": "user", "content": prompt, "system": system}]  
# make completion
completion = client.chat.completions.create(model=deployment, messages=messages)

# print response
print(completion.choices[0].message.content)

#  very unhappy _____.

# Once upon a time there was a very unhappy mermaid.
