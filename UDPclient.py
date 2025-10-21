#!/usr/bin/env python3.8.10
# -*- coding: utf-8 -*-
'''
@File    :   UDPclient.py
@Time    :   2025/09/15 20:05:58
@Author  :   disoXU 
@Version :   1.0
@Desc    :   None
'''

import socket               # 导入 socket 模块
import json
 
s = socket.socket(type=socket.SOCK_DGRAM)         # 创建 socket 对象
host = '10.31.242.211'       # 远程主机IP地址
port = 8081                 # 设置端口号

MyData = [1., 2., 3., 4.]   # 发送列表测试
json_Data = json.dumps(MyData).encode('utf-8')   # 转换为JSON字符串并编码
s.sendto(json_Data, (host, port))     # 发送消息给指定IP地址服务端
while 1: 
    # 发送消息
    send_msg = input("请输入要发送给服务端的消息：")
    send_msg = json.dumps(send_msg).encode("utf-8")  # 将发送的消息转换为JSON字符串
    s.sendto(send_msg, (host, port))
    if send_msg == "quit":
        break
    
    # 接受消息
    data = s.recv(1024).decode("utf-8")
    data = json.loads(data)
    print(f'服务端发送的消息:{data}')                           
s.close()