import cv2
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


api_key = "SG_acebee5324e7248c"
url = "https://api.segmind.com/v1/ssd-canny"

def generateImage(country, era, file_name):
    data = {
    "image": toB64(f'static/{country}/{file_name}'),
    "prompt": f"imagine this image painted in {country} style in {era} era",
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