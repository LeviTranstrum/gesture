import tflite_runtime.interpreter as tflite
import numpy as np
import time
from PIL import Image

interpreter = tflite.Interpreter(model_path='MediaPipeHandLandmarkDetector.tflite')
my_signature = interpreter.get_signature_runner()

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# check the type of the input tensor
floating_model = input_details[0]['dtype'] == np.float32

# NxHxWxC, H:1, W:2
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]
img = Image.open('test.jpg').resize((width, height))

# add N dim
input_data = np.expand_dims(img, axis=0)

if floating_model:
    input_data = (np.float32(input_data) - 127.5) / 127.5

interpreter.set_tensor(input_details[0]['index'], input_data)

start_time = time.time()
interpreter.invoke()
stop_time = time.time()

output_data = interpreter.get_tensor(output_details[0]['index'])
results = np.squeeze(output_data)

top_k = results.argsort()[-5:][::-1]
for i in top_k:
    if floating_model:
        print('{:08.6f}: {}'.format(float(results[i]), str(i)))
    else:
        print('{:08.6f}: {}'.format(float(results[i] / 255.0), str(i)))

print('time: {:.3f}ms'.format((stop_time - start_time) * 1000))