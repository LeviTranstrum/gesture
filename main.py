from finger_counter import finger_counter
from image_service import image_client
from ert3 import ert3
import yaml

def main():
    with open('/home/ert3/gesture/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    client = image_client.Image_Client(config) 
    controller = ert3.Ert3(config)
    counter = finger_counter.FingerCounter(config)
    min_confidence = config.get('min_confidence')

    count = None

    while(1):
        if controller.get_input(1):
            image = client.get_image()
            if image is None:
                controller.reset_outputs()
                controller.alarm_on()
                continue
                
            count, confidence, visualization_data = counter.count_fingers(image)
            if visualization_data is not None:
                client.send_visualization_data(visualization_data)
        
            controller.reset_outputs()

            if count is None or confidence < min_confidence:
                controller.alarm_on()
                continue   

            controller.alarm_off()
            
            if count > 0:
                controller.set_output(count, 1)

if __name__ == "__main__":
    main()