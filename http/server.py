# coding: utf8
import os
import SimpleHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import SocketServer

http_port = int(os.getenv('PORT') or 3000)

class SpiderHandler(BaseHTTPRequestHandler):
  def do_GET(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    s.wfile.write("""
      <html>
        <body>
          These are not the droids you're looking for...
        </body>
      </html>
    """)

def listen_and_serve():
  handler = SimpleHTTPServer.SimpleHTTPRequestHandler
  httpd = SocketServer.TCPServer(("", http_port), SpiderHandler)
  httpd.serve_forever()
