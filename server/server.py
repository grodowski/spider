# coding: utf8
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

http_port = int(os.getenv('PORT') or 3000)

class SpiderHandler(BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(
          """
            <html>
                <body>
                These are not the droids you're looking for...
                </body>
            </html>
          """.encode('utf-8')
        )

def listen_and_serve():
      httpd = HTTPServer(('', http_port), SpiderHandler)
      httpd.serve_forever()
