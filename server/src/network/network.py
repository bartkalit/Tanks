import socketserver


class Network(socketserver.StreamRequestHandler):

    def handle(self):
        print(self.client_address)
