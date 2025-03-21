import cv2
from http.server import SimpleHTTPRequestHandler, HTTPServer
import yaml
from . import image_service_config

# TODO: config.server and config.endpoint are not used here
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

            _, buffer = cv2.imencode('.jpg', frame)
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(buffer.tobytes())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == "__main__":
    with open('config.yaml', 'r') as file:
        config = image_service_config.ImageServiceConfig(yaml.safe_load(file))
    
    server_address = ('', config.port)
    httpd = HTTPServer(server_address, ImageServer)
    print(f"Starting server on port {config.port}...")
    httpd.serve_forever()
