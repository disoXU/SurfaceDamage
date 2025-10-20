#!/usr/bin/env python3.8.10
# -*- coding: utf-8 -*-
'''
@File    :   CVclient.py
@Time    :   2025/09/16 19:41:18
@Author  :   disoXU 
@Version :   1.0
@Desc    :   None
'''

import cv2
import socket                                     # 导入 socket 模块
import struct                                     # 用于处理二进制数据

s = socket.socket(type=socket.SOCK_DGRAM)         # 创建 socket 对象
host = '192.168.52.128'                           # 远程主机IP地址
port = 12347                                      # 设置端口号

img = cv2.imread('right.png')
img_encoded = cv2.imencode('.jpg', img)[1]        # [1]返回编码后的图像
# print(type(img_encoded))
img_bytes = img_encoded.tobytes()                      # 转换为字节流

# 发送文件头:
fhead = struct.pack('l', len(img_bytes))
s.sendto(fhead, (host, port))
print('发送文件头')

#循环发送图片码流
print('开始发送图片数据...')
for i in range(len(img_bytes)//1024+1):  # //为除法取整，+1包括小于1024字节的部分
    if 1024*(i+1) >= len(img_bytes):        
        # 最后不足1024字节的数据
        s.sendto(img_bytes[1024*i:], (host, port))
    else:
        # print(f'发送第{i+1}包数据')
        # 一次发送1024字节数据，python的切片不包括结尾
        s.sendto(img_bytes[1024*i:1024*(i+1)], (host, port)) 
    s.recv(1024)  # 等待服务端确认

print('图片数据发送完毕')
# s.sendto(img_bytes, (host, port))       # 发送消息给指定IP地址服务端
data = s.recv(1024)                     # 接收服务端确认消息
print(f'服务端发送的消息:{data.decode("utf-8")}')  
s.close()