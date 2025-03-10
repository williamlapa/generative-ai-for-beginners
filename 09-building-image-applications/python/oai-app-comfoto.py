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
        image_file.write(generated_image)  # Salva a imagem
    
    return image_path

def preprocess_image(image_path):
    """Converte a imagem para PNG e reduz o tamanho se necessário."""
    with Image.open(image_path) as img:
        # Converter para RGB se necessário
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        output_path = os.path.splitext(image_path)[0] + ".png"
        img.save(output_path, format="PNG")
        return output_path

def generate_from_real_image(image_path, output_name):
    processed_image_path = preprocess_image(image_path)
    
    response = client.images.create_variation(
        image=open(processed_image_path, "rb"),
        n=1,
        size="1024x1024"
    )
    
    variation_url = response.data[0].url  # Obtém a URL da nova imagem
    output_path = os.path.join(image_dir, output_name)
    
    generated_variation = requests.get(variation_url).content  # Baixa a imagem
    with open(output_path, "wb") as image_file:
        image_file.write(generated_variation)  # Salva a imagem
    
    return output_path

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

# --- Criando variação de uma foto real abaixo ---
real_image_path = "09-building-image-applications/python/foto.jpg"  # Substitua pelo caminho real da sua foto
if os.path.exists(real_image_path):
    new_image_path = generate_from_real_image(real_image_path, 'real-image-variation.png')
    image = Image.open(new_image_path)
    image.show()
else:
    print("Imagem real não encontrada. Envie uma foto válida.")
