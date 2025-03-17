from finger_counter import finger_counter
import yaml
import requests
import numpy as np
import cv2
# import m3io_py as m3io

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

URL = f"http://{config.get('image_server')}:{config.get('image_port')}/{config.get('endpoint')}"
output_slot = config.get('output_slot')
finger_config = config.get('finger_lengths')
counter = finger_counter.FingerCounter(finger_config)
prev_count = None

while(1):
    response = requests.get(URL)

    if response.status_code != 200:
        print(f'got status code {response.status_code}: {response.text}')
        continue

    # Convert the response content back to a NumPy array
    nparr = np.frombuffer(response.content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Decode as BGR (same as cv2.VideoCapture)
    if image is None:
        print("Failed to decode image")
        continue

    count = counter.count_fingers(image)
    if prev_count is not None and prev_count != count and prev_count > 0:
        # m3io.writeM3OutRelayP(0, output_slot, prev_count, 0)
        pass

    if count is None:
        print("failed to detect!")
        # m3io.setM3AlmLed(1)
        pass

    elif count > 0:
        print(count)
        # m3io.setM3AlmLed(0)
        # m3io.writeM3OutRelayP(0, output_slot, count, 1)
        pass

    prev_count = count