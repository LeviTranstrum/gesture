from finger_counter import finger_counter
from image_service import image_client
from ert3 import ert3

import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

client = image_client.Image_Client(config) 
controller = ert3.Ert3(config)
counter = finger_counter.FingerCounter(config)

count = None
prev_count = None

while(1):
    image = client.get_image()
    if image is None:
        continue

    count = counter.count_fingers(image)
    if prev_count is not None and prev_count != count and prev_count > 0:
        controller.set_output(prev_count, 0)

    if count is None:
        controller.alarm_on()

    elif count > 0:
        controller.alarm_off()
        controller.set_output(count, 1)

    prev_count = count