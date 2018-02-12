#!/usr/bin/python
#-*-coding:utf-8 -*-
import socket
import cv2
import numpy as np
from control.camera import Camera

class StreamClient:
    def __init__(self, stream_host = ('192.168.1.100', 8000)):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect(stream_host)

    def transfer(self, data):
        stringData = data.tostring()
        # 首先发送图片编码后的长度
        self.sock.send(str(str(len(stringData)).ljust(16)).encode())
        # 然后一个字节一个字节发送编码的内容
        # 如果是python对python那么可以一次性发送，如果发给c++的server则必须分开发因为编码里面有字符串结束标志位，c++会截断
        self.sock.send(stringData)
        
        data_r = self.sock.recv(50)
        print (data_r)

    def __del__(self):
        self.sock.close()
