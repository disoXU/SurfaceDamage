#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py
 
import socket               # 导入 socket 模块
 
s = socket.socket()         # 创建 socket 对象
host = '192.168.52.128'     # 绑定到所有端口
port = 12347                # 设置端口
s.bind((host, port))        # 绑定端口
 
# print(host)

s.listen(1)                 # 等待客户端连接
print("服务端已开始监听，正在等待客户端连接...")
c,addr = s.accept()         # 建立客户端连接
print(f"接收到了客户端的连接，客户端的IP地址：{addr}")

# 接受客户端信息，使用客户端和服务端的本次连接对象，而非 s 套接字对象
while True:
    # 接收消息
    data: str = c.recv(1024).decode("UTF-8")
    print(f"客户端发来的消息是：{data}")
    
    # 回复消息
    msg = input("请输入你要回复客户端的消息：")
    c.send(msg.encode('utf-8'))
    if msg == 'quit':
        break
c.close()               # 关闭连接
s.close()