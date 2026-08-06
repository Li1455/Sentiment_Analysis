import os
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add parent directory to sys.path to allow imports from app folder when run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.analyzer import SentimentAnalyzer

PORT = 8000
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Instantiate analyzer globally
analyzer = SentimentAnalyzer()

class SentimentAPIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override to log cleanly to stdout rather than standard stderr logging
        sys.stdout.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

    def send_json_response(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        # Support CORS just in case
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_OPTIONS(self):
        # CORS preflight requests
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        # Serve frontend files
        path = self.path
        if path == "/":
            path = "/index.html"

        # Sanitize path to prevent directory traversal
        sanitized_path = path.lstrip("/\\")
        sanitized_path = os.path.normpath(sanitized_path)
        if ".." in sanitized_path or sanitized_path.startswith("..") or os.path.isabs(sanitized_path):
            self.send_error(400, "Invalid Path")
            return

        file_path = os.path.join(STATIC_DIR, sanitized_path)

        if os.path.exists(file_path) and not os.path.isdir(file_path):
            # Determine content type
            if file_path.endswith(".html"):
                content_type = "text/html; charset=utf-8"
            elif file_path.endswith(".css"):
                content_type = "text/css; charset=utf-8"
            elif file_path.endswith(".js"):
                content_type = "application/javascript; charset=utf-8"
            elif file_path.endswith(".png"):
                content_type = "image/png"
            elif file_path.endswith(".ico"):
                content_type = "image/x-icon"
            else:
                content_type = "application/octet-stream"

            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, f"Internal error: {str(e)}")
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        if self.path == "/api/analyze":
            try:
                # Read content length
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length == 0:
                    self.send_json_response(400, {"error": "Missing request body."})
                    return

                # Read and parse body
                body_bytes = self.rfile.read(content_length)
                try:
                    body = json.loads(body_bytes.decode("utf-8"))
                except json.JSONDecodeError:
                    self.send_json_response(400, {"error": "Invalid JSON format."})
                    return

                # Check if body is a dictionary and has 'text' field
                if not isinstance(body, dict):
                    self.send_json_response(400, {"error": "Request body must be a JSON object."})
                    return

                if "text" not in body:
                    self.send_json_response(400, {"error": "Missing required field 'text'."})
                    return

                text_value = body["text"]

                # Perform analysis (validation checks inside analyzer.py)
                try:
                    result = analyzer.analyze(text_value)
                    self.send_json_response(200, result)
                except TypeError as te:
                    self.send_json_response(400, {"error": str(te)})
                except ValueError as ve:
                    self.send_json_response(400, {"error": str(ve)})

            except Exception as e:
                self.send_json_response(500, {"error": f"Internal Server Error: {str(e)}"})
        else:
            self.send_error(404, "Endpoint Not Found")

def run(port=PORT):
    # Ensure static directory exists
    os.makedirs(STATIC_DIR, exist_ok=True)
    
    server_address = ("", port)
    httpd = HTTPServer(server_address, SentimentAPIHandler)
    print(f"==================================================")
    print(f" Sentiment Analysis Web Server Running Successfully")
    print(f" URL: http://localhost:{port}")
    print(f" Stop the server: Press Ctrl+C")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()
        print("Server stopped.")

if __name__ == "__main__":
    # If run directly, run on default port
    run()
