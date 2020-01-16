host = '35.224.200.153'
#host = '10.146.1.202'
port = 5556

import socket
import time
from SimplePacket import SimplePacket



def convertToRaw(id,text):
    text = id + " " + text
    return text.encode()

def loop(client, reader):
    continueReading = True

    while continueReading:
        id, text = reader.read()
        raw = convertToRaw(id, text)

        print("Sending: ", raw)
        print("Response: ", client.send(raw))
        time.sleep(2)

    client.close()


class FakeReader:

    def __init__(self, reader=None):
        self.reader = reader

    def read(self):
        return "1","dog 15"

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

if __name__ == "__main__":
    client = Client(host, port)
    reader = FakeReader() # inlocuieste cu: SimpleMFRC522()
    loop(client,reader)