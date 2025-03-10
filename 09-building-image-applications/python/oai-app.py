from openai import OpenAI
import os
import requests
from PIL import Image
import dotenv

# import dotenv
dotenv.load_dotenv()
 
client = OpenAI()


try:
    # Create an image by using the image generation API
    generation_response = client.images.generate(
        model="dall-e-3",
        # prompt='Bunny on horse, holding a lollipop, on a foggy meadow where it grows daffodils', 
        prompt='Duas irmãs felizes, uma de 13 e outra de 17 anos, brincando na praia de Japaratinga, estado de Alagoas, em um dia ensolarado e bonito.',    # Enter your prompt text here
        size='1024x1024',
        n=1
    )
    # Set the directory for the stored image
    image_dir = os.path.join(os.curdir, 'images')

    # If the directory doesn't exist, create it
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # Initialize the image path (note the filetype should be png)
    image_path = os.path.join(image_dir, 'generated-image-william.png')

    # Retrieve the generated image
    print(generation_response)

    image_url = generation_response.data[0].url # extract image URL from response
    generated_image = requests.get(image_url).content  # download the image
    with open(image_path, "wb") as image_file:
        print("Escreve a imagem em bytes")
        print("-"*50)
        image_file.write(generated_image)

    # Display the image in the default image viewer
    image = Image.open(image_path)
    image.show()

# catch exceptions
except openai.InvalidRequestError as err:
    print(err)

# ---creating variation below---


response = client.images.create_variation(
  image=open(image_path, "rb"),
  n=2,
  size="1024x1024"
)

image_url = response.data[0].url  # Obtém a URL da nova imagem
generated_variation = requests.get(image_url).content  # Baixa a imagem
with open("images/variation.png", "wb") as image_file:
    image_file.write(generated_variation)  # Salva a imagem

image = Image.open("images/variation.png")
image.show()  # Exibe a imagem  
