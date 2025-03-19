import tflite_runtime.interpreter as tflite
import numpy as np
import cv2

class RTLite_Detector:
    def __init__(self):
        self.interpreter = tflite.Interpreter(model_path='MediaPipeHandLandmarkDetector.tflite')
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # check the type of the input tensor
        self.floating_model = self.input_details[0]['dtype'] == np.float32

        # NxHxWxC, H:1, W:2
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]

    def detect(self, image):
        img = cv2.resize(image, (self.width, self.height))
        # add N dim
        input_data = np.expand_dims(img, axis=0)

        if self.floating_model:
            input_data = (np.float32(input_data) - 127.5) / 127.5

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

        self.interpreter.invoke()

        landmarks = self.interpreter.get_tensor(self.output_details[2]['index'])  # Index 309 for landmarks
        results = np.squeeze(landmarks)  # Removes batch dimension
        results = [np.delete(results,2, axis=1).tolist()] # remove z dimension and convert to list

        return results