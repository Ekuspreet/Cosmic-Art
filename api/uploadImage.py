import requests

def upload_to_imgbb(image_path):
    imgbb_api_key = "30cdf95c0f7475b5040dc1b8b30f82b7"  # Replace with your ImgBB API key

    # ImgBB API endpoint
    api_url = "https://api.imgbb.com/1/upload"

    # Prepare the image data
    with open(image_path, "rb") as file:
        files = {"image": (image_path, file.read())}

    # Prepare the API request parameters
    params = {
        "key": imgbb_api_key,
    }

    try:
        # Make the POST request to ImgBB API
        response = requests.post(api_url, params=params, files=files)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

        # Parse the response JSON
        result = response.json()

        # Check if the upload was successful
        if result["success"]:
            image_url = result["data"]["url"]
            return image_url
        else:
            print("Upload failed. ImgBB API returned an error:", result)
            return None

    except requests.exceptions.RequestException as e:
        print("Error during ImgBB API request:", e)
        return None