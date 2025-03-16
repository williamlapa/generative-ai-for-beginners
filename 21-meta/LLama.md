Aqui está a tradução do arquivo  **README_LLAMA.md** , já incorporando as atualizações mais recentes do Llama 3.2 e 3.3.

---

# Construindo com a Família de Modelos Meta

## Introdução

Esta lição abordará:

* Exploração dos dois principais modelos da família Meta - **Llama 3.1** e  **Llama 3.2** .
* Compreensão dos casos de uso e cenários para cada modelo.
* Exemplos de código para demonstrar os recursos exclusivos de cada modelo.

---

## **A Família de Modelos Meta**

Nesta lição, exploraremos **dois modelos** da família Meta, também chamada de  **"Rebanho Llama"** : **Llama 3.1** e  **Llama 3.2** .

Esses modelos estão disponíveis em diferentes variantes no marketplace do GitHub Model. Veja mais detalhes sobre como usar GitHub Models para [prototipagem com IA](https://docs.github.com/en/github-models/prototyping-with-ai-models?WT.mc_id=academic-105485-koreyst).

### **Variantes dos Modelos:**

* **Llama 3.1 - 70B Instruct**
* **Llama 3.1 - 405B Instruct**
* **Llama 3.2 - 11B Vision Instruct**
* **Llama 3.2 - 90B Vision Instruct**

> *Nota: O Llama 3 também está disponível no GitHub Models, mas não será abordado nesta lição.*

---

## **Llama 3.1**

Com  **405 bilhões de parâmetros** , o **Llama 3.1** é um **LLM de código aberto** altamente avançado.

Esta versão aprimora o  **Llama 3** , trazendo:

* **Janela de contexto maior** → **128k tokens** vs  **8k tokens** .
* **Maior limite de saída** → **4096 tokens** vs  **2048 tokens** .
* **Melhor suporte multilíngue** → Graças ao aumento no volume de dados de treinamento.

Essas melhorias tornam o **Llama 3.1** ideal para aplicações avançadas de IA generativa, incluindo:

✅ **Chamadas de função nativas** → Capacidade de chamar ferramentas externas e APIs diretamente.

✅ **Melhor desempenho em RAG (Geração Aumentada por Recuperação)** → Devido à grande janela de contexto.

✅ **Geração de dados sintéticos** → Para melhorar tarefas como  **fine-tuning** .

---

### **Chamadas de Função Nativas (Function Calling)**

O **Llama 3.1** foi refinado para realizar chamadas de funções e ferramentas externas. Ele já inclui dois  **ferramentas nativas** :

🔍 **Brave Search** → Realiza buscas na web para obter informações atualizadas, como previsão do tempo.

📊 **Wolfram Alpha** → Resolve cálculos matemáticos complexos, eliminando a necessidade de criar funções personalizadas.

Também é possível criar **ferramentas personalizadas** que o modelo pode chamar.

#### Exemplo de Código: Chamando o Brave Search

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "meta-llama-3.1-405b-instruct"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

tool_prompt=f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Ambiente: ipython
Ferramentas: brave_search, wolfram_alpha
Data limite do conhecimento: Dezembro de 2023
Data de hoje: 23 de julho de 2024

Você é um assistente útil<|eot_id|>
"""

messages = [
    SystemMessage(content=tool_prompt),
    UserMessage(content="Qual é a previsão do tempo em Estocolmo?"),
]

response = client.complete(messages=messages, model=model_name)

print(response.choices[0].message.content)
```

---

## **Llama 3.2**

Apesar de ser um  **LLM** , o **Llama 3.1** **não suporta multimodalidade** (entrada de imagens e texto).

O **Llama 3.2** resolve essa limitação, permitindo  **processar imagens e texto simultaneamente** .

### **Principais Recursos do Llama 3.2:**

✅ **Multimodalidade** → Capacidade de entender imagens e texto.

✅ **Variantes de pequeno a médio porte** → Modelos de **11B** e **90B** parâmetros, oferecendo flexibilidade de implantação.

✅ **Versões somente texto (1B e 3B parâmetros)** → Permitem execução eficiente em  **dispositivos móveis e edge computing** , com baixa latência.

A adição do suporte multimodal representa um grande avanço no mundo dos  **LLMs open-source** .

#### Exemplo de Código: Processando Imagens com Llama 3.2

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    SystemMessage,
    UserMessage,
    TextContentItem,
    ImageContentItem,
    ImageUrl,
    ImageDetailLevel,
)
from azure.core.credentials import AzureKeyCredential

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "Llama-3.2-90B-Vision-Instruct"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = client.complete(
    messages=[
        SystemMessage(content="Você é um assistente útil que descreve imagens em detalhes."),
        UserMessage(
            content=[
                TextContentItem(text="O que há nesta imagem?"),
                ImageContentItem(
                    image_url=ImageUrl.load(
                        image_file="sample.jpg",
                        image_format="jpg",
                        detail=ImageDetailLevel.LOW)
                ),
            ],
        ),
    ],
    model=model_name,
)

print(response.choices[0].message.content)
```

---

## **🔥 Atualização: Lançamento do Llama 3.3 70B (Dezembro de 2024)**

A Meta lançou recentemente o  **Llama 3.3 70B** , um modelo otimizado com melhorias em eficiência e custo-benefício:

✅ **Desempenho comparável ao Llama 3.1 405B** → Mas com  **menor consumo de recursos** .

✅ **Melhoria no raciocínio e compreensão matemática** → Melhor desempenho em benchmarks de lógica.

✅ **Disponível no Amazon Bedrock** → Integração simplificada para aplicações empresariais.

🔗 Mais detalhes: [AWS Amazon](https://aws.amazon.com/pt/about-aws/whats-new/2024/12/metas-llama-3-3-70b-model-amazon-bedrock/?utm_source=chatgpt.com)

---

## **Continue sua Jornada no Aprendizado!**

Agora que você aprendeu sobre os modelos  **Llama 3.1, 3.2 e 3.3** , explore mais sobre IA generativa na nossa [coleção de aprendizado](https://aka.ms/genai-collection?WT.mc_id=academic-105485-koreyst).

🚀 **O futuro da IA generativa está na sua mão!** 🚀

---

Se precisar de mais alguma adaptação, me avise! 😃
