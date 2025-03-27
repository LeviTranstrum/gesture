from finger_counter import finger_counter
from image_service import image_client

import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

client = image_client.Image_Client(config) 
counter = finger_counter.FingerCounter(config)

while(1):
    image = client.get_image()

    count, confidence = counter.count_fingers(image)
    print(f"{count} fingers, {confidence*100}% sure")


