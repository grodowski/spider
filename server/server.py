# coding: utf8
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

from constants import REDIS as r

http_port = int(os.getenv('PORT') or 3000)

class SpiderHandler(BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

        s.wfile.write(
          f"""
            <html>
                <body>
                  {print(f"<p>{r.hgetall(key)}</p>") for key in r.keys()}
                </body>
            </html>
          """.encode('utf-8')
        )

def listen_and_serve():
      httpd = HTTPServer(('', http_port), SpiderHandler)
      httpd.serve_forever()
