import cv2
from http.server import SimpleHTTPRequestHandler, HTTPServer

class WebcamHandler(SimpleHTTPRequestHandler):
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
    server_address = ('', 8080)  # Run on port 8080
    httpd = HTTPServer(server_address, WebcamHandler)
    print("Starting server on port 8080...")
    httpd.serve_forever()
