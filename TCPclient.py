#!/usr/bin/env python3.8.10
# -*- coding: utf-8 -*-
'''
@File    :   TCPclient.py
@Time    :   2025/09/15 11:36:39
@Author  :   disoXU 
@Version :   1.0
@Desc    :   None
'''
 
import socket               # 导入 socket 模块
 
s = socket.socket()         # 创建 socket 对象
host = '10.31.242.211'       # 远程主机IP地址
port = 8080                 # 设置端口号
 
s.connect((host, port))     # 连接到服务端

while 1: 
    # 发送消息
    send_msg = input("请输入要发送给服务端的消息：")
    s.send(send_msg.encode("utf-8"))
    if send_msg == "quit":
        break

    # 接受消息
    data: str = s.recv(1024).decode("UTF-8")
    print(f'服务端发送的消息:{data}')
    if data == "quit":
        print("退出连接")
        break
s.close()

