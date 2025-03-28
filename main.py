from finger_counter import finger_counter
from image_service import image_client
from ert3 import ert3

import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

client = image_client.Image_Client(config) 
controller = ert3.Ert3(config)
counter = finger_counter.FingerCounter(config)
min_confidence = config.get('min_confidence')

count = None
prev_count = None

while(1):
    image = client.get_image()
    if image is None:
        controller.alarm_on()
        if prev_count is not None and prev_count > 0:
            controller.set_output(prev_count, 0)
        continue
        
    count, confidence, visualization_data = counter.count_fingers(image)
    if visualization_data is not None:
        client.send_visualization_data(visualization_data)
   
    if count is None or confidence < min_confidence:
        controller.alarm_on()
        if prev_count is not None and prev_count > 0:
            controller.set_output(prev_count, 0)
        continue   

    controller.alarm_off()
    if prev_count is not None and prev_count > 0:
        controller.set_output(prev_count, 0)
    
    if count > 0:
        controller.set_output(count, 1)

    prev_count = count