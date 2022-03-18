import socketserver

from server.src.network.network import Network


class Server:
    def __init__(self):
        self.clients = []
        self.network = socketserver.TCPServer(("127.0.0.1", 8080), Network)
        self.network.serve_forever()