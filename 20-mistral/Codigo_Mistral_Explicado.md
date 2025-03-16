Você enviou um arquivo Jupyter Notebook (`.ipynb`). Vou analisá-lo e explicar o código para você. Aguarde um momento enquanto faço isso.

### 📌 Explicação do Código no Notebook `githubmodels-assignment.ipynb`

Este notebook utiliza modelos da **Mistral AI** para **busca aumentada por recuperação (RAG)** e  **geração de código** , interagindo com APIs da  **Azure AI Inference** .

---

### 🚀 **Principais Componentes do Código**

1. **Instalação de Dependências**

   ```python
   !pip install faiss-cpu
   ```

   * Instala  **FAISS** , uma biblioteca eficiente para busca em espaços vetoriais.
2. **Importação de Bibliotecas**

   ```python
   import requests
   import numpy as np
   import faiss
   import os
   from azure.ai.inference import ChatCompletionsClient
   from azure.ai.inference.models import SystemMessage, UserMessage
   from azure.core.credentials import AzureKeyCredential
   from azure.ai.inference import EmbeddingsClient
   ```

   * Importa bibliotecas para manipulação de texto, embeddings e chamadas à API da Azure.
3. **Configuração da API da Azure**

   ```python
   endpoint = "https://models.inference.ai.azure.com"
   model_name = "Mistral-large"
   token = os.environ["GITHUB_TOKEN"]

   client = ChatCompletionsClient(
       endpoint=endpoint,
       credential=AzureKeyCredential(token),
   )
   ```

   * Define o endpoint da Azure e o modelo **Mistral Large** para inferência.
4. **Carregamento de Texto para RAG**

   ```python
   response = requests.get('https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt')
   text = response.text
   ```

   * Obtém um **ensaio do Paul Graham** do GitHub para ser usado como base de conhecimento.
5. **Divisão do Texto em Partes**

   ```python
   chunk_size = 2048
   chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
   ```

   * Divide o texto em pedaços de **2048 caracteres** para facilitar a busca.
6. **Geração de Embeddings**

   ```python
   embed_model_name = "cohere-embed-v3-multilingual"
   embed_client = EmbeddingsClient(endpoint=endpoint, credential=AzureKeyCredential(token))

   embed_response = embed_client.embed(input=chunks, model=embed_model_name)

   text_embeddings = np.array([item.embedding for item in embed_response.data])
   ```

   * Usa o modelo de embeddings da **Cohere** para converter texto em vetores numéricos.
7. **Criação de Índice FAISS**

   ```python
   d = text_embeddings.shape[1]
   index = faiss.IndexFlatL2(d)
   index.add(text_embeddings)
   ```

   * **FAISS** é usado para indexar os embeddings e permitir busca eficiente.
8. **Busca no Índice FAISS**

   ```python
   question = "저자가 대학에 오기 전에 주로 했던 두 가지 일은 무엇이었나요?？"

   question_embedding = embed_client.embed(input=[question], model=embed_model_name)
   question_embeddings = np.array(question_embedding.data[0].embedding)

   D, I = index.search(question_embeddings.reshape(1, -1), k=2)
   retrieved_chunks = [chunks[i] for i in I.tolist()[0]]
   ```

   * A pergunta é transformada em embeddings, e o  **FAISS retorna os trechos mais relevantes** .
9. **Geração de Resposta com o Mistral**

   ```python
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

   print(chat_response.choices[0].message.content)
   ```

   * Envia o **prompt estruturado** para o modelo  **Mistral Large** , que responde com base no contexto recuperado.

---

### **🏆 Outras Partes do Código**

1. **Comparação entre Mistral Small e Large**
   * Testa a latência e eficiência dos modelos **Mistral Small** e **Mistral Large** com o prompt `"Can you write a Python function to the fizz buzz test?"`.
2. **Teste de Tokenização com Mistral NeMo**
   * Compara a eficiência do tokenizador do **Mistral NeMo** com o do  **Mistral Large** .

---

### **💡 Resumo**

* **Objetivo** : O código usa **RAG** e **geração de código** com modelos  **Mistral** .
* **FAISS** : Permite busca eficiente por similaridade em grandes textos.
* **Azure AI** : Fornece inferência via API com modelos da Mistral.
* **Modelos usados** :  **Mistral Large** , **Mistral Small** e  **Mistral NeMo** .

Se precisar de mais detalhes ou ajustes no código, me avise! 🚀
