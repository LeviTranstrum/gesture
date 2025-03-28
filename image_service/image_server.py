import cv2
import numpy as np
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
import yaml
import threading
from . import image_service_config  # Adjust the import as needed

# Global variables to hold images
latest_captured_image = None
latest_annotated_image = None

def annotate_image_cv2(img, points, radius, size=2):
    # Colors in BGR order (from original RGB)
    colors = [(0, 0, 255), (0, 127, 255), (0, 255, 255),
              (0, 255, 0), (255, 0, 0), (0, 0, 0)]
    
    # Draw a small filled circle for each of the 6 points
    for i in range(min(6, len(points))):
        pt = points[i]
        x = int(pt["x"])
        y = int(pt["y"])
        cv2.circle(img, (x, y), size, colors[i], thickness=-1)
    
    # Draw the palm circle using the last color in the list
    center_pt = (int(points[-1]["x"]), int(points[-1]["y"]))
    cv2.circle(img, center_pt, int(radius), colors[5], thickness=size)
    
    return img

class ImageServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/capture':
            cap = cv2.VideoCapture(0)  # Open default webcam
            ret, frame = cap.read()
            cap.release()

            if not ret:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Failed to capture image")
                return

            # Update the global captured image
            global latest_captured_image
            latest_captured_image = frame

            # Encode the image as JPEG for the response
            _, buffer = cv2.imencode('.jpg', frame)
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(buffer.tobytes())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
    
    def do_POST(self):
        if self.path == '/show':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid JSON")
                return

            # Expecting only keypoints data in the POST (no image)
            if "keypoints" not in data:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing 'keypoints' field")
                return

            keypoints = data["keypoints"]
            if "points" not in keypoints or "palm_circle" not in keypoints:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing keypoints data")
                return

            points = keypoints["points"]  # List of dicts with "x" and "y"
            palm_circle = keypoints["palm_circle"]
            if "center" not in palm_circle or "radius" not in palm_circle:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing palm_circle data")
                return

            # Append the palm circle center to the points list so we have 6 points total
            points.append(palm_circle["center"])
            radius = palm_circle["radius"]

            # Use the last captured image from the GET /capture request
            global latest_captured_image
            if latest_captured_image is None:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No captured image available. Make a GET /capture request first.")
                return

            # Work on a copy of the captured image
            img = latest_captured_image.copy()

            # Annotate the image using OpenCV
            annotated_img = annotate_image_cv2(img, points, radius)

            # Update the global annotated image variable
            global latest_annotated_image
            latest_annotated_image = annotated_img

            # Display the annotated image in a reusable OpenCV window
            cv2.imshow("Annotated Image", latest_annotated_image)
            cv2.waitKey(1)  # Short wait to update the window

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Image annotated and displayed")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ImageServer)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    with open('config.yaml', 'r') as file:
        config = image_service_config.ImageServiceConfig(yaml.safe_load(file))
    
    # Create a reusable OpenCV window for annotated images
    cv2.namedWindow("Annotated Image", cv2.WINDOW_AUTOSIZE)
    
    run_server(config.port)
