import sublime
from os import path
import socket
from threading import Thread
import socketserver

server = None


class ConnectionHandler(socketserver.BaseRequestHandler):
    def handle(self):
        address = str(self.client_address)
        socket_fd = self.request.makefile("rb")
        
        pwd = socket_fd.readline().decode("utf8").strip()
        if len(pwd) == 0:
            return
        rel_path = socket_fd.readline().decode("utf8").strip()
        
        full_path = path.normpath(path.join(pwd, rel_path))
        if path.isdir(full_path):
                self.request.send(b"Cannot open folder\n")
        else:
            action = "Opening" if path.isfile(full_path) else "Creating"
            self.request.send(str.encode("{} {}\n".format(action, full_path)))
            sublime.active_window().open_file(full_path)

class TCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


def unload_handler():
    global server
    print('Killing server...')
    if server:
        server.shutdown()
        server.server_close()


def plugin_loaded():
    global server

    # Load settings
    settings = sublime.load_settings("local_subl.sublime-settings")
    port = settings.get("port", 52697)
    host = settings.get("host", "localhost")

    # Start server thread
    server = TCPServer((host, port), ConnectionHandler)
    Thread(target=server.serve_forever, args=[]).start()
    print('Server running on {}:{} ...'.format(host, str(port)))
