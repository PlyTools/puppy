# -*- coding: utf-8 -*-
from transfer.socket_server import *
from config import config

if __name__ == "__main__":
    videoServer = SocketServer().TCPServer(config.compu_ip, config.video_port, VideoStreamHandler)
    # ultraServer = SocketServer().TCPServer(config.compu_ip, config.ultra_port, UltraStreamHandler)

