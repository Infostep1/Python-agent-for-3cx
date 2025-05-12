from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser

PORT = 5000

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/trigger":
            # Ανοίγει το login.html στον browser
            webbrowser.open("http://localhost:5000/login.html")

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Login popup triggered")
        elif self.path == "/login.html":
            # Εξυπηρετεί τη login σελίδα
            with open("static/login.html", "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    print(f"Listening on http://localhost:{PORT}/trigger")
    server = HTTPServer(('0.0.0.0', PORT), RequestHandler)
    server.serve_forever()
