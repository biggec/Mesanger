import struct
import socket


class Connection:
    def __init__(self, conn, addr=None):
        self.connection = conn
        self.addr = addr

    def send(self, data):
        if self.connection:
            if type(data) == str:
                send_string(self.connection, data)
            else:
                send_data(self.connection, data)

    def receive_string(self):
        if self.connection:
            return receive_string(self.connection)

    def receive_data(self):
        if self.connection:
            return receive_string(self.connection)

    def close(self):
        if self.connection:
            self.connection.close()


class Server:
    def __init__(self, port, host=''):
        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.socket.listen(10)
        self.addr = None

    def accept(self):
        connection, addr = self.socket.accept()
        return connection, addr


class Client:
    def __init__(self, host, port):
        connection = socket.socket()
        connection.connect((host, port))
        self.connection = Connection(connection)


def send_data(sock, data):
    size = len(data)
    size_bytes = struct.pack(">I", size)
    sock.send(size_bytes)
    sock.send(data)


def receive_data(sock):
    size_bytes = sock.recv(4)
    if not size_bytes:
        return b''
    size = struct.unpack('>I', size_bytes)[0]

    data = b''
    while len(data) != size:
        data += sock.recv(size)

    return data


def send_string(sock, s):
    send_data(sock, s.encode('utf-8'))


def receive_string(sock):
    return receive_data(sock).decode('utf-8')
