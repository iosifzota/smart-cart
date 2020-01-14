
class SimplePacket:
    def __init__(self):
        # constants
        self.FIXED_HEADER_SIZE = 8
        #
        self.reset()


    def reset(self):
        # the received data
        self.content = None
        # what is *sent* on the "wires"
        self.buffer = b''

        # setup for reading
        self._expectedByteCount = self.FIXED_HEADER_SIZE
        self._stage = self._readFixedHeader

    def readyStage(self):
        return self._stage == self.readyStage

    def _updateStage(self, nextStage, stageByteCount):
        self._stage = nextStage # next stage
        self._expectedByteCount = stageByteCount

    def _appendData(self, data):
        self.buffer += data

    def _canRead(self):
        if self._expectedByteCount is None:
            print("No need to read more bytes.")
            return False
        if len(self.buffer) < self._expectedByteCount:
            print("Need at least", self._expectedByteCount, "bytes.")
            return False
        return True

    def _readData(self):
        """ Extract bytes from the buffer. """
        # Debug. This fn should be called only after checking canRead()
        if not self._canRead():
            raise Exception("Trying to read more data than there is.")

        data = self.buffer[:self._expectedByteCount]
        self.buffer = self.buffer[self._expectedByteCount:]

        return data

    def _readFixedHeader(self):
        if not self._canRead():
            return False
        nextByteCount = int.from_bytes(self._readData(), byteorder="little", signed=False)
        self._updateStage(self._readContent, nextByteCount)
        return True

    def _readContent(self):
        if not self._canRead():
            return False
        self.content = self._readData()

        self._updateStage(self.readyStage, None)
        return True

    def read(self, data):
        self._appendData(data)

        while not self.readyStage():
            if not self._stage():
                print("Warn: Stage failed")
                return False
        return True

    def pack(self, content):
        self.reset()
        contentLen = len(content)

        self.buffer = contentLen.to_bytes(length=self.FIXED_HEADER_SIZE, byteorder="little")
        if type(content) is not bytes:
            self.content = bytes(content)
        else:
            self.content = content

        self.buffer += self.content

        self._updateStage(self.readyStage, None)