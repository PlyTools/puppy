# -*- coding: utf-8 -*-
import socket
import cv2
import numpy as np

class SocketClient:
    
    def TCPClient(self, host, port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host, port))
        return self

    def send(self, stringData):
        # send the length of stringData after encoded
        self.sock.sendall(bytes(str(len(stringData)).ljust(16), "utf-8"))
        # send the data
        self.sock.sendall(stringData)


    def __del__(self):
        self.sock.close()
