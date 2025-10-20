#!/usr/bin/env python3.8.10
# -*- coding: utf-8 -*-
'''
@File    :   CVserver.py
@Time    :   2025/09/16 19:54:35
@Author  :   disoXU 
@Version :   1.0
@Desc    :   None
'''

import cv2
import numpy as np
import socket               # 导入 socket 模块 
import struct

s = socket.socket(type=socket.SOCK_DGRAM)         # 创建 socket 对象
host = '192.168.52.128'       # 本地主机IP地址
port = 12347                  # 设置端口号
s.bind((host, port))          # 绑定端口
print("等待接收消息...")
# data, addr = s.recvfrom(65536)               # 接收数据
# print(f'接收自{addr}的数据')

while True:
# 接收文件头，文件头的长度由calcsize函数确定
    fhead_size = struct.calcsize('l')
    buf, addr = s.recvfrom(fhead_size)

    # unpack结果是一个元组，所以需要把值取出来
    data_size = struct.unpack('l', buf)[0]
    print(f'图片字节数:{data_size}, 来自{addr}')
    
    # 接收图片码流长度的码流
    recvd_size = 0    # 已接收的字节数
    data_total = b''  # 接收的字节数据排列到这里
    print('开始接收图片...')

    # 直到接收字节数等于图片字节数再停止接收
    while not recvd_size == data_size:
        if data_size - recvd_size >1024:
            data, addr = s.recvfrom(1024)
            recvd_size += len(data)
        else:
            # 最后不足1024字节的数据
            data, addr = s.recvfrom(1024)
            recvd_size = data_size  
        s.sendto(b'ok', addr)  # 回发数据，防止丢包
        data_total += data
    if recvd_size == data_size:
        print('图片接收完成')
        break

np_array = np.frombuffer(data_total, np.uint8)        # 将字节数据转换为numpy数组
img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)  # 解码图像

s.sendto(b'Image received', addr)            # 发送确认消息

cv2.imshow('Received Image', img)            # 显示图像
cv2.waitKey(0)
cv2.destroyAllWindows()
s.close()
