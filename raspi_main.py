# -*- coding: utf-8 -*-
import os
import subprocess
from control.pid import PID
from control.car_servo import Car_Servo
from control.car import Car

pid = PID(1, 0.1, 1.5)
car = Car()
servo = Car_Servo()

if __name__ == "__main__":
    from control.ultrasonic import Ultrasound
    from transfer.socket_client import SocketClient
    from config import config
    from transfer.socket_server import *
    from control.camera import Camera
    
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