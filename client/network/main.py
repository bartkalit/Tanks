import socket

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 8080))
    data = input('You: ')
    sock.send(data.encode())
    received = sock.recv(1024)
    print('Received: ', received.decode())