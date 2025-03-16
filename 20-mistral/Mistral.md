# Construindo com Modelos Mistral

## Introdução

Esta lição abordará:

* Exploração dos diferentes modelos Mistral.
* Compreensão dos casos de uso e cenários para cada modelo.
* Exemplos de código mostrando os recursos exclusivos de cada modelo.

## Os Modelos Mistral

Nesta lição, exploraremos três modelos Mistral diferentes:

 **Mistral Large** , **Mistral Small** e  **Mistral NeMo** .

Cada um desses modelos está disponível gratuitamente no marketplace de modelos do GitHub. O código neste notebook utilizará esses modelos para demonstração. Aqui estão mais detalhes sobre como usar o GitHub Models para [prototipar com modelos de IA](https://docs.github.com/en/github-models/prototyping-with-ai-models?WT.mc_id=academic-105485-koreyst).

---

## **Mistral Large 2 (2407)**

O **Mistral Large 2** é atualmente o modelo principal da Mistral, projetado para uso corporativo.

Este modelo é uma melhoria do Mistral Large original, oferecendo:

* **Janela de contexto maior** → 128k tokens vs 32k tokens.
* **Melhor desempenho em tarefas matemáticas e de programação** → 76,9% de precisão média vs 60,4%.
* **Suporte multilíngue aprimorado** → Idiomas suportados: Inglês, Francês, Alemão, Espanhol, Italiano, Português, Holandês, Russo, Chinês, Japonês, Coreano, Árabe e Hindi.

Com esses recursos, o **Mistral Large 2** se destaca em:

* **Geração aumentada por recuperação (RAG)** → Graças à sua grande janela de contexto.
* **Chamada de funções (Function Calling)** → Integração nativa com ferramentas e APIs externas, permitindo chamadas paralelas ou sequenciais.
* **Geração de código** → Excelente desempenho na geração de código em  **Python, Java, TypeScript e C++** .

### Exemplo de RAG usando o Mistral Large 2

Este exemplo usa o Mistral Large 2 para aplicar um padrão de **RAG (Retrieval-Augmented Generation)** sobre um documento de texto. A pergunta está em coreano e questiona as atividades do autor antes da faculdade.

O código utiliza o **modelo de embeddings da Cohere** para criar embeddings tanto do documento quanto da pergunta. O armazenamento vetorial é feito usando  **faiss** . O prompt enviado ao modelo Mistral inclui a pergunta e os trechos recuperados mais relevantes. O modelo então gera uma resposta em linguagem natural.

```python
pip install faiss-cpu
```


```python
import requests
import numpy as np
import faiss
import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import EmbeddingsClient

endpoint = "https://models.inference.ai.azure.com"
model_name = "Mistral-large"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = requests.get('https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt')
text = response.text

chunk_size = 2048
chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
len(chunks)

embed_model_name = "cohere-embed-v3-multilingual" 

embed_client = EmbeddingsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token)
)

embed_response = embed_client.embed(
    input=chunks,
    model=embed_model_name
)



text_embeddings = []
for item in embed_response.data:
    length = len(item.embedding)
    text_embeddings.append(item.embedding)
text_embeddings = np.array(text_embeddings)


d = text_embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(text_embeddings)

question = "저자가 대학에 오기 전에 주로 했던 두 가지 일은 무엇이었나요?？"

question_embedding = embed_client.embed(
    input=[question],
    model=embed_model_name
)

question_embeddings = np.array(question_embedding.data[0].embedding)


D, I = index.search(question_embeddings.reshape(1, -1), k=2) # distance, index
retrieved_chunks = [chunks[i] for i in I.tolist()[0]]

prompt = f"""
Context information is below.
---------------------
{retrieved_chunks}
---------------------
Given the context information and not prior knowledge, answer the query.
Query: {question}
Answer:
"""


chat_response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content=prompt),
    ],
    temperature=1.0,
    top_p=1.0,
    max_tokens=1000,
    model=model_name
)

print(chat_response.choices[0].message.content)import
```

(O código continua...)

---

## **Mistral Small**

O **Mistral Small** é outro modelo da família Mistral, classificado como um  **Small Language Model (SLM)** .

### **Vantagens do Mistral Small** :

* **Mais econômico** → 80% de redução de custo em relação ao Mistral Large e NeMo.
* **Baixa latência** → Respostas mais rápidas em comparação com modelos maiores da Mistral.
* **Flexível** → Pode ser implantado em diferentes ambientes, exigindo menos recursos.

### **Casos de uso ideais** :

* **Tarefas baseadas em texto** , como sumarização, análise de sentimento e tradução.
* **Aplicações com chamadas frequentes** → Devido ao custo reduzido.
* **Tarefas de código de baixa latência** , como revisão e sugestões de código.

---

## **Comparando Mistral Small e Mistral Large**

Abaixo, há um teste para comparar a latência entre **Mistral Small** e  **Mistral Large** .

A diferença no tempo de resposta pode variar entre  **3 a 5 segundos** , além das diferenças no estilo e tamanho da resposta.

```python
import os 
endpoint = "https://models.inference.ai.azure.com"
model_name = "Mistral-small"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = client.complete(
    messages=[
        SystemMessage(content="Você é um assistente útil para programação."),
        UserMessage(content="Você pode escrever uma função em Python para o teste FizzBuzz?"),
    ],
    temperature=1.0,
    top_p=1.0,
    max_tokens=1000,
    model=model_name
)

print(response.choices[0].message.content)
```

O mesmo código pode ser executado para  **Mistral Large** , alterando `model_name = "Mistral-large"`.

---

## **Mistral NeMo**

O **Mistral NeMo** é um modelo de código aberto com  **licença Apache2** , sendo considerado uma evolução do  **Mistral 7B** .

### **Principais características do Mistral NeMo** :

* **Tokenização mais eficiente** → Usa o **Tekken tokenizer** em vez do mais comum `tiktoken`, proporcionando melhor desempenho para múltiplos idiomas e código.
* **Ajustável por fine-tuning** → O modelo base está disponível para ajuste fino, permitindo maior flexibilidade em aplicações personalizadas.
* **Suporte nativo a Function Calling** → Assim como o Mistral Large, pode chamar funções externas.

---

### **Comparando Tokenizadores**

Este exemplo compara como o **Mistral NeMo** e o **Mistral Large** lidam com tokenização.

O **NeMo retorna menos tokens** para o mesmo prompt, demonstrando sua eficiência.

```bash
pip install mistral-common
```

```python
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer

# Tokenizador Mistral NeMo
model_name = "open-mistral-nemo"
tokenizer = MistralTokenizer.from_model(model_name)

# Exemplo de tokenização
tokenized = tokenizer.encode_chat_completion(
    ChatCompletionRequest(
        messages=[UserMessage(content="Como está o tempo hoje em Paris?")],
        model=model_name,
    )
)

tokens, text = tokenized.tokens, tokenized.text
print(len(tokens))  # Exibe a contagem de tokens
```

Para comparar com  **Mistral Large** , basta trocar `model_name = "mistral-large-latest"`.

---

## **Aprendizado contínuo: Continue sua jornada!**

Após concluir esta lição, explore mais sobre IA generativa na nossa [coleção de aprendizado](https://aka.ms/genai-collection?WT.mc_id=academic-105485-koreyst).

---

### 🚀  **Resumo** :

* **Mistral Large 2** → Modelo poderoso para empresas, com grande janela de contexto e suporte a várias línguas.
* **Mistral Small** → Modelo compacto e eficiente, ideal para tarefas rápidas e custo reduzido.
* **Mistral NeMo** → Modelo open-source, otimizado para tokenização e  **fine-tuning** .

Se precisar de mais alguma informação ou explicação sobre os conceitos, me avise! 🚀
