import cv2
import numpy as np


# 读取原图，w, h
src_img = cv2.imread('lenna.png')
w, h, channels = src_img.shape
# 创建等大空白图
dst_img = np.zeros([800, 800, channels], np.uint8)
# 将原图按比例等分
w_rate = float(w) / 800
h_rate = float(h) / 800
for i in range(800):
    for j in range(800):
        x = int(i * w_rate + 0.5)
        y = int(j * h_rate + 0.5)
        dst_img[i, j] = src_img[x, y]

cv2.imshow('nearst', dst_img)
cv2.waitKey(0)