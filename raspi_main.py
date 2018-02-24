# -*- coding: utf-8 -*-
from control.camera import Camera
from control.ultrasonic import Ultrasound
from transfer.socket_client import SocketClient
from transfer.socket_server import *
import os
import subprocess
from config import config


if __name__ == "__main__":
    # receive lane params and control kitte to movie
    print("Create TCP Server thread to receive params stream")
    paramsServer = SocketServer().TCPServer(config.raspi_ip, config.paras_port, ParamsStreamHandler)

    # # os.system('tools/remote_camera.sh')
    # sub = subprocess.Popen('tools/remote_camera.sh')

    # create a client for video stream transmission
    print("Create TCP Client thread to send video stream")
    camera = Camera()
    videoClient = SocketClient().TCPClient(config.compu_ip, config.video_port)

    # # create a client for ultrasound sensor data transmission
    # ultrasound = Ultrasound()
    # ultraClient = SocketClient().TCPClient(config.compu_ip, config.ultra_port)

    print("Running...")
    # send data
    while True:
        videoClient.send(camera.getFrameArray())
    #     ultraClient.send(ultrasound.get_distance())