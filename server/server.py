# coding: utf8
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

from constants import REDIS as r
from server.renderer import Renderer

http_port = int(os.getenv('PORT') or 3000)

class SpiderHandler(BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html; charset=utf-8")
        s.end_headers()
        s.wfile.write(

          f"""
            <!DOCTYPE html>
            <html>
                <body>
                    <p>OtoDom items:</p>
                    <table>
                        {s.render_items()}
                    </table>
                </body>
            </html>
          """.encode('utf-8')
        )

    def render_items(self):
        items = []
        for key in r.keys():
            items.append(r.hgetall(key))
        return Renderer().render(items)


def listen_and_serve():
      httpd = HTTPServer(('', http_port), SpiderHandler)
      httpd.serve_forever()
