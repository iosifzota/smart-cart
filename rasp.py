import selectors
import types
from SimplePacket import SimplePacket
import socket
import time

sel = selectors.DefaultSelector()
packetCreator = SimplePacket()


host = '10.146.1.90'
port = 5556

class Client:

    def __init__(self, host, port):
        self.sock, self.data = startConnections(host, port, 1)[0]

        self.FIXED_HEADER_SIZE = 8

    def send(self, msg):
        if self.sock is None:
            print("[Info]No socket")
            return

        msglen = int.to_bytes(len(msg), self.FIXED_HEADER_SIZE, byteorder="little")
        self.sock.sendall(msglen + msg)

        self._getResp()

    def _getResp(self):
        if self.sock is None:
            print("[Info]No socket")
            return

        while True:
            changedList = sel.select(timeout=None)  # wait for response

            for key, eventsMask in changedList:
                if eventsMask & selectors.EVENT_WRITE:
                    # done reading
                    # prepare for next read
                    self.data.packet.reset()
                    sel.modify(self.sock, selectors.EVENT_READ, data=self.data)
                    return

                serviceConnection(key, eventsMask)


    def close(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None

def createSessionData(connid):
    return types.SimpleNamespace(
        connid=connid,
        packet=SimplePacket(),
        outb=b'',
    )

def startConnections(host_, port_, numConns):
    svrAddr = (host_, port_)
    sockets = []
    for i in range(0, numConns):
        connid = i + 1
        # setup socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)  # non-blocking socket

        print("starting connection", connid, "to", svrAddr)
        sock.connect_ex(svrAddr)
        # setup params
        eventsMask = selectors.EVENT_READ # listen only for reading always
        data = createSessionData(connid)
        # register sockets for events
        sel.register(sock, eventsMask, data=data)

        sockets.append((sock, data)) # save sock ref

    return sockets

def serviceConnection(key, eventsMask):
    sock = key.fileobj
    data = key.data
    # processResponse
    if eventsMask & selectors.EVENT_READ:
        recvData = sock.recv(1024)     # Should be ready to read
        if recvData:
            # print("received", repr(recvData), "from connection", data.connid, "+")
            data.packet.read(recvData)
            # check if packet was fully read
            if data.packet.readyStage():
                print("Result:")
                print(data.packet.content)
                # Done reading a packet
                if data.packet.buffer:
                    print("Response was too long/more packets where send.")
                    print("Discarding extra.")
                # listen for write events to prevent sel.select from blocking.
                sel.modify(sock, selectors.EVENT_WRITE, data=data)
        # if not recvData (connection closed abruptly by the server):
        else:
            print("closing connection", data.connid)
            sel.unregister(sock)
            sock.close()
    else:
        raise Exception('[Debug]Listening only for read events.')

def eventLoop(c):
    try:
        while True:
            changed = sel.select(timeout=None)

            if changed:
                for key, eventsMask in changed:
                    serviceConnection(key, eventsMask)
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()

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

if __name__ == "__main__":
    client = Client(host, port)
    reader = FakeReader() # inlocuieste cu: SimpleMFRC522()
    loop(client,reader)