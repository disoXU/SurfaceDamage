#!/usr/bin/env python3.8.10
# -*- coding: utf-8 -*-
'''
@File    :   Surface.py
@Time    :   2025/09/29 09:37:11
@Author  :   disoXU 
@Version :   1.0
@Desc    :   None
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt
# plt.rcParams.update({"font.size":20}) #此处必须添加此句代码方可改变标题字体大小
# mpl.rcParams['font.sans-serif'] = ['simsun']  # 用来正常显示中文标签
# mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 读取图像
img1 = cv2.imread('plane1.png')
img2 = cv2.imread('plane2.png')

# 转为灰度图
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# 高斯滤波
gray1 = cv2.GaussianBlur(gray1, (0, 0), 2)
gray2 = cv2.GaussianBlur(gray2, (0, 0), 2)

# 二值化
_, binary_img1 = cv2.threshold(gray1, 200, 255, cv2.THRESH_BINARY)
_, binary_img2 = cv2.threshold(gray2, 200, 255, cv2.THRESH_BINARY)

# 图像差分获得损伤区域
diff_img = cv2.absdiff(binary_img1, binary_img2)

# 创建子图
plt.figure(figsize=(12, 10))

plt.subplot(2, 2, 1)
plt.imshow(diff_img, cmap='gray')
plt.title('图像差分得到的损伤区域', fontproperties='Simsun', fontsize = 20)
plt.axis('off')

# 形态学操作：先闭运算再开运算
se1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
se2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

closed_img = cv2.morphologyEx(diff_img, cv2.MORPH_CLOSE, se1)
opened_img = cv2.morphologyEx(closed_img, cv2.MORPH_OPEN, se2)

plt.subplot(2, 2, 2)
plt.imshow(opened_img, cmap='gray')
plt.title('形态学操作后的损伤区域', fontproperties='SimHei')
plt.axis('off')

# 连通域分析
num_labels, labeledImage = cv2.connectedComponents(opened_img // 255)
minArea = 10000  # 面积阈值
valid_centroids = []  # 存储符合条件的质心

# 创建结果图像
img_fault = np.zeros_like(opened_img)

# 遍历所有连通域
for i in range(1, num_labels):  # 跳过背景(0)，背景区域标为0
    # 提取当前连通域
    mask = (labeledImage == i).astype(np.uint8) * 255
    
    # 计算面积
    area = cv2.countNonZero(mask)
    
    # 保留面积大于阈值的区域
    if area >= minArea:
        img_fault += mask
        
        # 计算质心
        M = cv2.moments(mask)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            valid_centroids.append((cX, cY))

plt.subplot(2, 2, 3)
plt.imshow(img_fault, cmap='gray')
plt.title('损伤区域', fontproperties='Simsun')
plt.axis('off')

# 计算并显示损伤面积
area = cv2.countNonZero(img_fault)
print(f"损伤面积为{area}个像素点")

# 寻找边界并绘制
plt.subplot(2, 2, 4)
# 转换为RGB以便正确显示颜色
img_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.title('损伤区域边界与质心', fontproperties='Simsun')
plt.axis('off')

# 寻找轮廓，返回N*1*2的numpy数组
contours, _ = cv2.findContours(img_fault, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 绘制边界
for contour in contours:
    # 将轮廓转换为适合matplotlib的格式
    contour = contour.squeeze() # 删除多余的维度，将contours变成N*2的numpy数组
    if len(contour.shape) == 1:  # 处理单个点的情况
        continue
    plt.plot(contour[:, 0], contour[:, 1], 'r', linewidth=1.5)

# 绘制质心和坐标
for (cX, cY) in valid_centroids:
    plt.plot(cX, cY, 'bo', markersize=4, markerfacecolor='k')
    plt.text(cX + 10, cY + 10, f'({cX},{cY})', color='b', fontsize=10)

plt.tight_layout()
plt.show()
