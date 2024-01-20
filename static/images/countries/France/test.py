import requests
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

# Request payload
data = {
  "image": toB64('static\images\countries\France\Dance-at-Le-moulin-de-la-Galette-Bal-du-moulin-de-la-Galette-by-Pierre-Auguste-Renoir.jpg'),
  "prompt": "futuristic",
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
print(response)