from http.server import CGIHTTPRequestHandler
from http.server import ThreadingHTTPServer
from typing import Optional, Callable, Any


class MyHTTPRequestHandler(CGIHTTPRequestHandler):

    def __init__(self,
                 *args,
                 is_cors: bool = True,
                 is_logging: bool = False,
                 get_handler: Optional[Callable[['MyHTTPRequestHandler'], None]] = None,
                 post_handler: Optional[Callable[['MyHTTPRequestHandler'], None]] = None,
                 directory=None,
                 **kwargs):
        self.is_cors = is_cors
        self.is_logging = is_logging
        self.get_handler = get_handler
        self.post_handler = post_handler
        super().__init__(*args, directory=directory, **kwargs)

    def end_headers(self):
        if self.is_cors:
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_GET(self):
        self.get_handler(self) if self.get_handler else super().do_GET()

    # noinspection PyPep8Naming
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        self.post_handler(self) if self.post_handler else super().do_POST()

    def log_message(self, ft: str, *args: Any):
        if self.is_logging:
            super().log_message(ft, *args)


class Server(ThreadingHTTPServer):

    # noinspection PyTypeChecker
    def __init__(self,
                 host: str = '0.0.0.0',
                 port: int = 8080,
                 is_cors: bool = True,
                 is_logging: bool = False,
                 get_handler: Optional[Callable[[MyHTTPRequestHandler], None]] = None,
                 post_handler: Optional[Callable[[MyHTTPRequestHandler], None]] = None,
                 static_dir: str = None):
        super().__init__((host, port), lambda *args, **kwargs: MyHTTPRequestHandler(*args,
                                                                                    is_cors=is_cors,
                                                                                    is_logging=is_logging,
                                                                                    get_handler=get_handler,
                                                                                    post_handler=post_handler,
                                                                                    directory=static_dir,
                                                                                    **kwargs))

    def start(self) -> 'Server':
        self.serve_forever()
        return self

    def close(self):
        self.shutdown()
        self.server_close()
