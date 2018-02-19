# -*- coding: utf-8 -*-
from transfer.socket_server import *


if __name__ == "__main__":
    videoServer = SocketServer().TCPServer('192.168.1.100', 8000, VideoStreamHandler)
    # ultraServer = SocketServer().TCPServer('192.168.1.100', 8002, UltraStreamHandler)

