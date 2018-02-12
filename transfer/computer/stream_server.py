#!/usr/bin/python
#-*-coding:utf-8 -*-
import socket
import cv2
import numpy


class StreamServer:
    # 接受图片大小的信息
    def __init__(self, stream_host = ('192.168.1.100', 8000)):
        self.stream_host = stream_host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置地址与端口，如果是接收任意ip对本服务器的连接，地址栏可空，但端口必须设置
        self.sock.bind(self.stream_host) # 将Socket（套接字）绑定到地址
        self.sock.listen(1) # 开始监听TCP传入连接
        print ('Waiting for connection...')
        # 接受TCP链接并返回（conn, addr），其中conn是新的套接字对象，可以用来接收和发送数据，addr是链接客户端的地址。
        self.conn, self.addr = self.sock.accept()
        print("Connection from: ", self.addr)

    def recv_size(self, sock, count):
        buf = b''
        buf = sock.recv(count)
        if not buf: return None
        return buf

    def receive(self):
        while 1:
            length = self.recv_size(self.conn, 16).decode() #首先接收来自客户端发送的大小信息
            if isinstance (length, str): #若成功接收到大小信息，进一步再接收整张图片
                stringData = self.recv_size(self.conn, int(length))
                data = numpy.fromstring(stringData, dtype='uint8')
                decimg=cv2.imdecode(data, 1)         #解码处理，返回mat图片
                # cv2.imshow('SERVER', decimg)
                cv2.imwrite('received.jpeg', decimg)
                print('Image recieved successfully!')
                self.conn.send("Server has recieved messages!".encode())

    def __del__(self):
        self.sock.close()
        cv2.destroyAllWindows()
    
if __name__ == "__main__":
    stream_host = ('192.168.1.100', 8000)
    streamServer = StreamServer(stream_host)
    streamServer.receive()