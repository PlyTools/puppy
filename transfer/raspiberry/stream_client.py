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

    def send(self, data):
        stringData = data.tostring()
        # send the length of image after encoded
        self.sock.send(str(str(len(stringData)).ljust(16)).encode())
        # send the data
        self.sock.send(stringData)
        
        data_r = self.sock.recv(50)
        print (data_r)

    def __del__(self):
        self.sock.close()
