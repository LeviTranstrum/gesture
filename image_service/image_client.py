import requests
from PIL import Image
from io import BytesIO
from image_service_config import ImageServiceConfig

class Image_Client:
    def __init__(self, config):
        self.config = ImageServiceConfig(config)
        self.URL = f"http://{config.get('image_server')}:{config.get('image_port')}/{config.get('endpoint')}"

    def get_image(self):
        response = requests.get(self.URL)

        if response.status_code != 200:
            print(f'got status code {response.status_code}: {response.text}')
            return None

        # Convert the response content into a PIL image
        image = Image.open(BytesIO(response.content))
        if image is None:
            print("Failed to decode image")
        
        return image