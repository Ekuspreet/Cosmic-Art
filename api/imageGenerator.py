from PIL import Image
import requests
from io import BytesIO
from base64 import b64encode

def toB64(image_path):
    if image_path is None:
        return
    else:
        with open(image_path, "rb") as image_file:
            # Read the image file
            image_data = image_file.read()

            # Encode the image data to base64
            b64_encoded = b64encode(image_data)

            # Convert bytes to string and remove unnecessary characters
            return b64_encoded.decode("utf-8")


api_key = "SG_3dd20dabed54c3c2"
url = "https://api.segmind.com/v1/ssd-canny"
prompts = {"Ancient": "Transform the given image into the Ancient era, incorporating classical architecture reminiscent of Greek or Roman structures, mythical elements such as dragons or gods, and clothing styles characteristic of ancient civilizations.",
    "Medieval": "Adapt the existing image to the Medieval era, introducing knights in armor, medieval castle structures with Gothic architecture, heraldic symbols, and a landscape that conveys the ambiance of medieval times.",
    "Renaissance": "Give the current image a Renaissance makeover, featuring classical art and architecture, elaborate Renaissance clothing, and incorporating scientific and artistic elements reflective of the cultural rebirth of the Renaissance era.",
    "Futuristic": "Transform the image into a futuristic scene, integrating advanced technology, sleek futuristic cityscapes, high-tech gadgets, innovative transportation, and cutting-edge fashion styles.",
    "Contemporary": "Update the image to the Contemporary era, incorporating modern urban landscapes, scenes depicting diverse cultures, contemporary fashion trends, everyday life with technology devices, and current architectural styles.",
    "Modern": "Evolve the image to represent the Modern era, highlighting technological advancements, scenes of contemporary city life, the multicultural fabric of society, modern architecture, global connectivity, and reflections of current events in culture."
  }

def generateImage(country, era, file_name):
    prompt = prompts[era]
    data = {
    "image": toB64(f'static/images/countries/{country}/{file_name}'),
    "prompt": f'{prompt}, {country} style',
    "negative_prompt": "low quality, ugly, painting",
    "samples": 1,
    "scheduler": "UniPC",
    "num_inference_steps": 30,
    "guidance_scale": 7.5,
    "seed": 760941192,
    "controlnet_scale": 0.5,
    "base64": False
    }

    response = requests.post(url, json=data, headers={'x-api-key': api_key})
    image = Image.open(BytesIO(response.content))
    return image