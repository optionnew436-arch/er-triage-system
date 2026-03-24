# Simple local server to view the dashboard
# Run: python serve.py
import http.server
import socketserver
import webbrowser
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

print(f"Starting server at http://localhost:{PORT}")
print("Opening dashboard in browser...")
print("Press Ctrl+C to stop.\n")

webbrowser.open(f"http://localhost:{PORT}/dashboard.html")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
