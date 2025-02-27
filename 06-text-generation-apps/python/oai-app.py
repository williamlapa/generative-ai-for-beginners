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
prompt = "Complete the following: Once upon a time there was uma linda senhora brasileira chamada Luciana Maria que morava em Recife, adorava carnaval, mas pensava demais na vida e a idade às vezes criava medos"
messages = [{"role": "user", "content": prompt}]  
# make completion
completion = client.chat.completions.create(model=deployment, messages=messages)

# print response
print("Era uma vez uma linda senhora brasileiria chamda Luciana Maria que morava em Recife, adorava carnaval, mas pensava demais na vida e a idade às vezes criava medos " + completion.choices[0].message.content)

#  very unhappy _____.

# Once upon a time there was a very unhappy mermaid.
