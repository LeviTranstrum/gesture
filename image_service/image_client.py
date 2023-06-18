import requests
from PIL import Image
from io import BytesIO
from  . import image_service_config

class Image_Client:
    def __init__(self, config):
        self.config = image_service_config.ImageServiceConfig(config)
        self.URL = f"http://{self.config.server}:{self.config.port}"
        self.image_endpoint = self.config.image_endpoint
        self.visualization_endpoint = self.config.visualization_endpoint

    def get_image(self):
        try:
            response = requests.get(f"{self.URL}/{self.image_endpoint}")

            if response.status_code != 200:
                print(f'got status code {response.status_code}: {response.text}')
                return None

            # Convert the response content into a PIL image
            image = Image.open(BytesIO(response.content))
            if image is None:
                print("Failed to decode image")
            
            return image
    
        except Exception as e:
            print("Error getting image:", e)
            return None
    
    def send_visualization_data(self, visualization_data):
        try:
            response = requests.post(
                f"{self.URL}/{self.visualization_endpoint}",
                json=visualization_data
            )
            return response
        except Exception as e:
            print("Error sending visualization:", e)
            return None
