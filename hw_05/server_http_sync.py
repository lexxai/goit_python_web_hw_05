from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import urllib.parse
import mimetypes
import json
import logging
from datetime import datetime
import socket

BASE_ROOT_DIR = Path("html")


class WWWHandler(BaseHTTPRequestHandler):
    socket_client = None

    def save_data(self, data) -> bool:
        result = self.socket_client.run_socket_client(data)
        return result

    def get_file(self, filename, state=200):
        # print(f"{BASE_ROOT_DIR=}")
        self.send_response(state)
        mmtype, _ = mimetypes.guess_type(filename)
        if mmtype:
            self.send_header("Content-Type", mmtype)
        else:
            self.send_header("Content-Type", "plain/text")
        self.end_headers()
        try:
            with open(filename, "rb") as fp:
                self.wfile.write(fp.read())
        except Exception as e:
            logger.error(e)

    def do_POST(self):
        route_path = urllib.parse.urlparse(self.path)
        match route_path.path:
            case "/message":
                cont_len = int(self.headers["Content-Length"])
                data = self.rfile.read(cont_len)
                result = self.save_data(data)
                location = "/message_done.html" if result else "/error.html"
                self.send_response(301)
                self.send_header("Location", location)
                self.end_headers()

            case _:
                self.send_response(301)
                self.send_header("Location", "/error.html")
                self.end_headers()

    def do_GET(self):
        route_path = urllib.parse.urlparse(self.path)
        match route_path.path:
            case "/":
                filename = BASE_ROOT_DIR / "index.html"
                self.get_file(filename)
            case _:
                filename = BASE_ROOT_DIR / route_path.path[1:]
                if filename.exists():
                    self.get_file(filename)
                else:
                    filename = BASE_ROOT_DIR / "error.html"
                    self.get_file(filename, 404)


def run(server=HTTPServer, handler=WWWHandler):
    global logger
    logger = logging.getLogger(__name__)
    address = ("", 8000)
    http_server = server(address, handler)
    logger.info(f"Start HTTP server at port: {address[1]}")
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
    except Exception as e:
        logger.error(e)
        http_server.server_close()

logger: logging

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s [ %(threadName)s ] %(message)s"
    )
    run()
