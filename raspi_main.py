# -*- coding: utf-8 -*-
from control.camera import Camera
from control.ultrasonic import Ultrasound
from transfer.socket_client import SocketClient
from transfer.socket_server import *


if __name__ == "__main__":
    # print("Create TCP Server thread to receive params stream")
    # raspi_ip = '192.168.1.111'
    # # receive lane params and control kitte to movie
    # paramsServer = SocketServer().TCPServer(raspi_ip, 8000, ParamsStreamHandler)

    print("Create TCP Client thread to send video stream")
    compu_ip = '192.168.1.103'
    # create a client for video transfer
    camera = Camera()
    videoClient = SocketClient().TCPClient(compu_ip, 8000)

    # # create a client for ultrasound sensor transfer
    # ultrasound = Ultrasound()
    # ultraClient = SocketClient().TCPClient(compu_ip, 8002)

    print("Running...")
    # send data
    while True:
        print(camera.getFrameArray().tostring())
        print(type(camera.getFrameArray().tostring()))
        videoClient.send(camera.getFrameArray().tostring())
        break
        # ultraClient.send(ultrasound.get_distance())

