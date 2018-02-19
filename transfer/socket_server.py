#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import cv2
import socketserver
import sys
import numpy as np
import threading
sys.path.append("../")
from transfer.socket_client import SocketClient
from lane.laneline_coord import *
from config import config


class VideoStreamHandler(socketserver.BaseRequestHandler):

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
            if isinstance(length, str): #若成功接收到大小信息，进一步再接收整张图片
                stringData = self.recv_size(self.request, int(length))
                data = np.fromstring(stringData, dtype='uint8')
                img = cv2.imdecode(data, 1)         #解码处理，返回mat图片
                # cv2.imshow('SERVER', img)
                # cv2.imwrite('received.jpeg', img)
                print('Image recieved successfully!')
                params = processImage(img, M, initParams, refPos)
                print("Server has recieved message!")
                # send params to raspiberry
                self.paramsClient.send(str(params).encode())

class UltraStreamHandler(socketserver.BaseRequestHandler):

    def recv_size(self, sock, count):
        buf = b''
        buf = sock.recv(count)
        if not buf: return None
        return buf

    def handle(self):
        while True:
            length = self.recv_size(self.request, 16).decode() #首先接收来自客户端发送的大小信息
            if isinstance (length, str): #若成功接收到大小信息，进一步再接收整张图片
                streamData = self.recv_size(self.request, int(length))
                ultraDistance = float(streamData)
                print("Distance: %0.1f cm" % ultraDistance)

                self.request.send("Server has recieved distance!".encode())

class ParamsStreamHandler(socketserver.BaseRequestHandler):

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
                params = str(streamData)
                print(params)
                print("Server has recieved message!")
                # TODO:Control kitte according to params

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