#!/usr/bin/python
#-*-coding:utf-8 -*-
import socket
import cv2
import numpy

stream_host = ('192.168.1.100', 8000)

# socket.AF_INET用于服务器与服务器之间的网络通信
# socket.SOCK_STREAM代表基于TCP的流式socket通信
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 连接服务端
sock.connect(stream_host)

# 从摄像头采集图像
frame = cv2.imread("1.jpeg")

# 首先对图片进行编码，因为socket不支持直接发送图片
result, imgencode = cv2.imencode('.jpeg', frame)
data = numpy.array(imgencode)
stringData = data.tostring()
# 首先发送图片编码后的长度
sock.send(str(str(len(stringData)).ljust(16)).encode())
# 然后一个字节一个字节发送编码的内容
# 如果是python对python那么可以一次性发送，如果发给c++的server则必须分开发因为编码里面有字符串结束标志位，c++会截断
sock.send(stringData)
#cv2.imshow('CLIENT',frame)
# if cv2.waitKey(10) == 27:
#     break
# 接收server发送的返回信息
data_r = sock.recv(50)
print (data_r)

sock.close()
