import socket
from SimplePacket import SimplePacket

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("starting connection to ", (host,port))

        self.sock.connect((host,port))
        self.packetCreator = SimplePacket()

    def send(self, data):
        self.packetCreator.pack(data)
        print("Sending ", self.packetCreator.buffer)
        self.sock.sendall(self.packetCreator.buffer)

    def close(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None

