# -*- coding: utf-8 -*-
from transfer.socket_server import *


if __name__ == "__main__":
    compu_ip = '192.168.1.103'
    videoServer = SocketServer().TCPServer(compu_ip, 8000, VideoStreamHandler)
    # ultraServer = SocketServer().TCPServer(compu_ip, 8002, UltraStreamHandler)

