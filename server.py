import socket
import selectors
import types
from SimplePacket import SimplePacket
from cart import Cart

host = '10.146.1.90'
port = 5556

shoppingCart = Cart()

# Get best select() function
sel = selectors.DefaultSelector()
# Used for packing response
packetCreator = SimplePacket()

def setupSock(host_, port_):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host_, port_))
    return sock

def acceptConnection(sock):
    """Accept a connection on @sock and register it for READ & WRITE events."""
    conn, addr = sock.accept()
    print("Accepted connection from", addr)

    # setup session data
    data = types.SimpleNamespace(
        addr=addr,
        tosend=b"",
        packet=SimplePacket()
    )

    # listen for READ events on conn socket
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, data=data)


def processRequest(sock, data):
    """ Process client request. Called when READ even is triggered on @sock."""
    recvData = sock.recv(1024)
    if recvData:
        # print("received", repr(recvData), "from address", data.addr, "+")
        data.packet.read(recvData)
        # check if packet was fully read
        if data.packet.readyStage():
            # print("Received packet successfully.")
            # print("Header:")
            # print(data.packet.header)
            # print("Content:")
            # print(data.packet.content)
            # done reading a packet
            if data.packet.buffer:
                print("Request was too long/more packets where send.")
                print("Discarding extra.")
            print("Read:", data.packet.content)  # here do whatever with the data
            shoppingCart.scan(data.packet.content)
            # listen for write event now
            sel.modify(sock, selectors.EVENT_WRITE, data=data)
    else:
        print("Closing connection to", data.addr)
        sel.unregister(sock)
        sock.close()


def response(sock, data):
    """ Send response after processingRequest. Called when WRITE event is triggered on @sock (which is always on any
    sock). """
    if not data.tosend:
        if not data.packet.readyStage():
            print("Err")
        #taskNr = int(data.packet.content) - 1
        #resData = b'response: ' + data.packet.content
        resData = data.packet.content
        packetCreator.pack(resData)
        data.tosend = packetCreator.buffer
    if data.tosend:
        # print("sending", repr(data.tosend), "to", data.addr)
        sentBytesCount = sock.send(data.tosend)
        data.tosend = data.tosend[sentBytesCount:]  # drop sent bytes
        if not data.tosend:
            # print("send successful")
            # Now listen for a request
            data.packet = SimplePacket()
            sel.modify(sock, selectors.EVENT_READ, data=data)


def service_connection(key, eventsMask):
    """ Service the connection: set it up or processRequest and respond."""
    sock = key.fileobj
    data = key.data
    if eventsMask & selectors.EVENT_READ:
        processRequest(sock, data)
    if eventsMask & selectors.EVENT_WRITE:
        response(sock, data)


def eventLoop():
    try:
        while True:
            changedList = sel.select(timeout=None)  # None -> block until an event is triggered
            for key, eventsMask in changedList:
                if key.data is None:
                    sock = key.fileobj
                    acceptConnection(sock)
                else:
                    service_connection(key, eventsMask)
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()


def main():
    serverSock = setupSock(host, port)
    print("Listening on", f'{host}:{port}')
    serverSock.listen()

    # listen for READ events on socket
    serverSock.setblocking(False)   # non-blocking socket
    sel.register(serverSock, selectors.EVENT_READ, data=None)

    eventLoop()


if __name__ == "__main__":
    main()
