from openai import OpenAI
import os
import requests
from PIL import Image
import dotenv

dotenv.load_dotenv()
 
client = OpenAI()

# Definir diretório global para armazenar as imagens
image_dir = os.path.join(os.curdir, 'images')
os.makedirs(image_dir, exist_ok=True)

def generate_image(prompt, image_name):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size='1024x1024',
        n=1  # Apenas 1 imagem por requisição
    )
    
    image_url = response.data[0].url  # Pega a URL da imagem gerada
    image_path = os.path.join(image_dir, image_name)
    
    generated_image = requests.get(image_url).content  # Baixa a imagem
    with open(image_path, "wb") as image_file:
        print("Escreve a imagem em bytes")
        print("-"*50)
        image_file.write(generated_image)  # Salva a imagem
    
    return image_path

try:
    prompt = 'Duas irmãs felizes, uma de 13 e outra de 17 anos, brincando na praia de Japaratinga, estado de Alagoas, em um dia ensolarado e bonito.'
    
    # Gerar duas imagens separadamente
    image_paths = [
        generate_image(prompt, 'generated-image-1.png'),
        generate_image(prompt, 'generated-image-2.png')
    ]
    
    # Exibir as imagens geradas
    for path in image_paths:
        image = Image.open(path)
        image.show()

except OpenAI.APIError as err:
    print(f"Erro na API: {err}")

# ---creating variation below---

variation_paths = []

for path in image_paths:
    response = client.images.create_variation(
        image=open(path, "rb"),
        n=1,  # Criar apenas 1 variação por requisição
        size="1024x1024"
    )
    
    variation_url = response.data[0].url  # Obtém a URL da nova imagem
    variation_path = os.path.join(image_dir, f'variation-{os.path.basename(path)}')
    
    generated_variation = requests.get(variation_url).content  # Baixa a imagem
    with open(variation_path, "wb") as image_file:
        print("REGERA a imagem em bytes")
        print("-"*50)
        image_file.write(generated_variation)  # Salva a imagem
    
    variation_paths.append(variation_path)

# Exibir as variações geradas
for path in variation_paths:
    image = Image.open(path)
    image.show()
