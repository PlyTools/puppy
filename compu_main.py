# -*- coding: utf-8 -*-
from transfer.socket_server import *
import lane.laneline_coord_bku1 as bku1
from config import config

if __name__ == "__main__":
    videoServer = SocketServer().TCPServer(config.compu_ip, config.video_port, VideoStreamHandler)
    
    # ultraServer = SocketServer().TCPServer(config.compu_ip, config.ultra_port, UltraStreamHandler)