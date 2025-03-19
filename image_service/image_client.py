import requests
import cv2
import numpy as np

class Image_Client:
    def __init__(self, URL):
        self.URL = URL

    def get_image(self):
        response = requests.get(self.URL)

        if response.status_code != 200:
            print(f'got status code {response.status_code}: {response.text}')
            return None

        # Convert the response content back to a NumPy array
        nparr = np.frombuffer(response.content, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Decode as BGR (same as cv2.VideoCapture)
        if image is None:
            print("Failed to decode image")
        
        return image