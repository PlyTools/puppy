# -*- coding: utf-8 -*-
from control.camera import Camera
from control.ultrasonic import Ultrasound
from transfer.socket_client import SocketClient
from transfer.socket_server import *


if __name__ == "__main__":
    # receive lane params and control kitte to movie
    paramsServer = SocketServer().TCPServer('192.168.1.111', 8000, ParamsStreamHandler)

    # create a client for video transfer
    camera = Camera()
    videoClient = SocketClient().TCPClient('192.168.1.100', 8000)

    # # create a client for ultrasound sensor transfer
    # ultrasound = Ultrasound()
    # ultraClient = SocketClient().TCPClient('192.168.1.100', 8002)

    # send data
    while True:
        videoClient.send(camera.getFrameArray().tostring())
        # ultraClient.send(ultrasound.get_distance())

