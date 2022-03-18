class User:
    def __init__(self, client):
        self.ip, self.port = client
        print(self.ip, self.port)