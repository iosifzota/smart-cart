#host = '10.146.1.36'
host = '35.246.183.183'
#host = '10.146.1.202'
port = 5556

import socket
import time

def convertToRaw(id,text):
    text = id + " " + text
    return text.encode()

def loop(client, reader):
    continueReading = True

    while continueReading:
        raw = reader.read()
        print("Sending: ", raw)
        print("Response: ", client.send(raw))
        time.sleep(10)

    client.close()


class FakeReader:

    def __init__(self, reader=None):
        self.reader = reader

    def read(self):
        return b'1 dog 15\n'

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("starting connection to ", (host,port))

        self.sock.connect((host,port))

    def send(self, data):
        self.sock.sendall(data)

    def close(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None

if __name__ == "__main__":
    client = Client(host, port)
    reader = FakeReader() # inlocuieste cu: SimpleMFRC522()
    loop(client,reader)