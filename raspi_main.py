#-*-coding:utf-8 -*-
from control.camera import Camera
from control.ultrasonic import Ultrasound
from transfer.socket_client import SocketClient


if __name__ == "__main__":
    # create a client for video transfer
    camera = Camera()
    videoClient = SocketClient().TCPClient('192.168.1.100', 8000)

    # # create a client for ultrasound sensor transfer
    # ultrasound = Ultrasound()
    # ultraClient = SocketClient().TCPClient('192.168.1.100', 8002)

    # send data
    while True:
        videoClient.sendVideo(camera.getFrameArray())
        # ultraClient.sendUltra(ultrasound.get_distance())

