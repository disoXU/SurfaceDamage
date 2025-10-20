#!/usr/bin/env python3.8.10
# -*- coding: utf-8 -*-
'''
@File    :   UDPServer.py
@Time    :   2025/09/15 19:47:04
@Author  :   disoXU 
@Version :   1.0
@Desc    :   None
'''

import socket               # 导入 socket 模块
import json
 
s = socket.socket(type=socket.SOCK_DGRAM)         # 创建 socket 对象
host = '192.168.52.128'     # 绑定到所有端口
port = 12347                # 设置端口
s.bind((host, port))        # 绑定端口

# UDP通信不需要先连接，所以没有conn对象，服务端发送消息必须指定address且只能用sendto()方法
# 所以要先知道发消息给你的客户端IP地址，使用recvfrom()方法会用元组接受数据和客户端地址
while True:
    # 接收消息
    data, addr = s.recvfrom(1024)
    data = json.loads(data.decode('utf-8'))      # 解码并转换为原始数据类型

    print(f"客户端的IP地址是：{addr}")
    print(f"客户端发来的{type(data).__name__}消息是：{data}")
    if type(data) == list: continue

    # 回复消息
    msg = input("请输入你要回复客户端的消息：")
    msg = json.dumps(msg).encode('utf-8')     # 转换为JSON字符串
    s.sendto(msg, addr)    # 发送消息给指定IP地址客户端
    if msg == 'quit':
        break
s.close()               # 关闭连接