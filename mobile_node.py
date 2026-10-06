import http.server
import socketserver

PORT = 8081
Handler = http.server.SimpleHTTPRequestHandler

print(f"[*] NomaanOS Satellite Node listening on port {PORT}...")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
