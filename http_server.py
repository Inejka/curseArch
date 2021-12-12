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

        # GET sends back a Hello world message

    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}).encode('utf-8'))

        # POST echoes the message adding a JSON field

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        # refuse to receive non-json content
        # if ctype != 'application/json':
        #    self.send_response(400)
        #    self.end_headers()
        #    return

        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        print(message)
        ans = app.execute(message["command"], message["args"])
        # add a property to the object, just to mess with data
        to_return = {'ans': ans}

        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(to_return).encode('utf-8'))


def main():
    PORT = 8000
    server_address = ('localhost', PORT)
    server = HTTPServer(server_address, request_handler)
    print("Server running on port %s" % PORT)
    server.serve_forever()


main()
