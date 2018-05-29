# -*- coding: utf-8 -*-
import re
import socket
import cv2
import socketserver
import sys
import numpy as np
import threading
sys.path.append("../")
from config import config
from lane.laneline_coord import *
from transfer.socket_client import SocketClient

class VideoStreamHandler(socketserver.BaseRequestHandler):
    # global label = 0
    # 接受图片大小的信息
    def recv_size(self, sock, count):
        buf = b''
        # buf = sock.recv(count)
        # if not buf: return None
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def handle(self):
        if not config.parasInit:
            self.paramsClient = SocketClient().TCPClient(config.raspi_ip, config.paras_port)
            config.parasInit = True
        while True:
            length = self.recv_size(self.request, 16).decode()  #首先接收来自客户端发送的大小信息
            if isinstance(length, str):                         #若成功接收到大小信息，进一步再接收整张图片
                bytesData = self.recv_size(self.request, int(length))
                # print(bytesData)
                img = cv2.imdecode(np.fromstring(bytesData, dtype=np.uint8), flags=1)   #解码处理，返回mat图片
                # cv2.imshow('SERVER', img)
                print('Image recieved successfully!')
                config.params = processImage(img, M, config.params, refPos)
                print("Server has recieved message!")
                cv2.imwrite('temp/socket/' + str(config.params[2]) + " " + str(config.params[3]) + ".jpeg", img)
                # send params to raspiberry
                self.paramsClient.send(str(config.params).encode())

class UltraStreamHandler(socketserver.BaseRequestHandler):

    def recv_size(self, sock, count):
        buf = b''
        buf = sock.recv(count)
        if not buf: return None
        return buf

    def handle(self):
        while True:
            length = self.recv_size(self.request, 16).decode()  #首先接收来自客户端发送的大小信息
            if isinstance (length, str):                        #若成功接收到大小信息，进一步再接收整张图片
                streamData = self.recv_size(self.request, int(length))
                ultraDistance = float(streamData)
                print("Distance: %0.1f cm" % ultraDistance)

                self.request.send("Server has recieved distance!".encode())

class ParamsStreamHandler(socketserver.BaseRequestHandler):
    def setup(self):
        from raspi_main import car, pid, servo
        self.car = car
        self.servo = servo
        self.pid = pid

    def recv_size(self, sock, count):
        buf = b''
        buf = sock.recv(count)
        if not buf: return None
        return buf

    def handle(self):
        while True:
            length = self.recv_size(self.request, 16).decode() 
            if isinstance (length, str):
                streamData = self.recv_size(self.request, int(length))
                print(re.sub(r' +', " ", bytes.decode(streamData).replace('\n', ' ')))
                params = np.array(re.sub(r' +', " ", bytes.decode(streamData).replace('\n', ' ')).split(" "))
                print(params[4])
                offset = self.pid.update(float(params[4]))
                print("Server has recieved message!")
                print(90 + offset)
                self.car.set_duty_cycle(7)
                self.servo.set_angle(90 + offset)


class SocketServer(object):

    def TCPServer(self, host, port, Handler):
        self.server = socketserver.ThreadingTCPServer((host, port), Handler)
        server = threading.Thread(target = self.server.serve_forever)
        server.start()
        # self.server.serve_forever()
        return self

if __name__ == "__main__":
    videoServer = SocketServer().TCPServer(config.compu_ip, config.video_port, VideoStreamHandler)
    # ultraServer = SocketServer().TCPServer(config.compu_ip, config.ultra_port, UltraStreamHandler)