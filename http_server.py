from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi
import app

app = app.app("server_user")


class request_handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        print(message)
        ans = app.execute(message["command"], message["args"])
        to_return = {'ans': ans}
        self._set_headers()
        self.wfile.write(json.dumps(to_return).encode('utf-8'))

def main():
    PORT = 8000
    server_address = ('localhost', PORT)
    server = HTTPServer(server_address, request_handler)
    print("Server running on port %s" % PORT)
    server.serve_forever()


main()
