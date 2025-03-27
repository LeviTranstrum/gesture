from finger_counter import finger_counter
from image_service import image_client
from ert3 import test_ert3

import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

client = image_client.Image_Client(config) 
controller = test_ert3.Test_Ert3(config)
counter = finger_counter.FingerCounter(config)

count = None
prev_count = None
test_image_count = 0

while(1):
    image = client.get_image()
    if image is None:
        continue

    image.save(f"test/images/{test_image_count}.png", format="png")
    test_image_count = test_image_count + 1

    count = counter.count_fingers(image)
    if prev_count is not None and prev_count != count and prev_count > 0:
        controller.set_output(prev_count, 0)

    if count is None:
        controller.alarm_on()

    elif count > 0:
        controller.alarm_off()
        controller.set_output(count, 1)

    prev_count = count