# -*- coding: utf-8 -*-
from transfer.socket_server import *
import lane.laneline_coord_bku1 as bku1
from config import config

if __name__ == "__main__":
    # videoServer = SocketServer().TCPServer(config.compu_ip, config.video_port, VideoStreamHandler)
    paramsClient = SocketClient().TCPClient(config.raspi_ip, config.paras_port)
    params = bku1.processImage(bku1.hoststr, bku1.M, bku1.initParams, bku1.refPos)
    paramsClient.send(str(params).encode())
    
    # ultraServer = SocketServer().TCPServer(config.compu_ip, config.ultra_port, UltraStreamHandler)