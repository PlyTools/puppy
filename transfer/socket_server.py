#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import cv2
import numpy
import socketserver

class VideoStreamHandler(socketserver.BaseRequestHandler):
    
    def recv_size(self, sock, count):
        buf = b''
        buf = sock.recv(count)
        if not buf: return None
        return buf

    def handle(self):
        while True:
            length = self.recv_size(self.request, 16).decode() #首先接收来自客户端发送的大小信息
            if length: #若成功接收到大小信息，进一步再接收整张图片
                streamData = self.recv_size(self.request, int(length))
                data = numpy.fromstring(streamData, dtype='uint8')
                decimg=cv2.imdecode(data, 1)         #解码处理，返回mat图片
                
                # cv2.imshow('SERVER', decimg)
                cv2.imwrite('received.jpeg', decimg)
                print('Image recieved successfully!')
                self.request.send("Server has recieved messages!".encode())

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
                streamData = self.recv_size(self.request, int(length.decode()))
                ultraDistance = float(streamData)
                print("Distance: %0.1f cm" % ultraDistance)

                self.request.send("Server has recieved distance!".encode())

class SocketServer(object):
    def TCPServer(self, host, port, Handler):
        self.server = socketserver.ThreadingTCPServer((host, port), Handler)
        self.server.serve_forever()
        return self

if __name__ == "__main__":
    videoServer = SocketServer().TCPServer('192.168.1.100', 8000, VideoStreamHandler)
    # ultraServer = SocketServer().TCPServer('192.168.1.100', 8002, UltraStreamHandler)