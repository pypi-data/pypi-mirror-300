import socket
import threading
from typing import List, Tuple, Union

zero = chr(0)

class Connect:

    def __init__(self, addr: str, sock: socket.socket):
        self.sock: socket.socket = sock
        self.addr: Tuple[str, int] = addr
        self.remainning_s: str = ""

    def __del__(self):
        self.sock.close()

    def recv(self) -> str:
        s: str = self.remainning_s
        ret_s: str = ""
        while 1:
            try:
                s += self.sock.recv(1024).decode("utf-8")
            except Exception:
                return s
            if zero in s:
                ret_s, self.remainning_s = s.split(zero, 1)
                return ret_s

    def send(self, s: str) -> bool:
        try:
            self.sock.send((s + zero).encode("utf-8"))
            return True
        except Exception:
            return False


class Host:
    ip: Union[str, None]
    port: Union[int, None]
    sock: socket.socket
    connects: List[Connect]
    strpipe: List[Tuple[Connect, str]]
    __stop_accept: bool

    def __init__(self, ip: Union[str, None] = None, port: Union[int, None] = None):
        self.addr = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connects = []
        self.strpipe = []
        self.__stop_accept = True

    def __del__(self):
        self.sock.close()

    def __add_connect(self, connect: Connect) -> bool:
        self.connects.append(connect)
        threading.Thread(target=self.__recv, args=(connect,)).start()

    def __recv(self, connect: Connect) -> None:
        while 1:
            self.strpipe.append((connect, connect.recv()))

    def __accept(self) -> None:
        while not self.__stop_accept:
            sock, addr = self.sock.accept()
            self.__add_connect(Connect(addr, sock))

    def accept(self) -> None:
        self.sock.bind(self.addr)
        self.sock.listen()
        self.__stop_accept = False
        threading.Thread(target=self.__accept).start()

    def stop_accept(self) -> None:
        self.__stop_accept = True

    def connect(self, ip: str, port: int) -> bool:
        try:
            self.sock.connect((ip, port))
            self.__add_connect(Connect(None, self.sock))
            return True
        except Exception:
            return False

    def send_all(self, s: str) -> None:
        for connect in self.connects:
            connect.send(s)

    def send_by_index(self, index: int, s: str) -> None:
        self.connects[index].send(s)

    def pop_str(self) -> Tuple[Connect, str]:
        if len(self.strpipe) == 0:
            return None
        return self.strpipe.pop(0)
