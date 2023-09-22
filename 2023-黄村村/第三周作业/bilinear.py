import cv2
import numpy as np

# 实现双线性插值

# 读图
src_img = cv2.imread('lenna.png')
w, h, channels = src_img.shape
# 创建空白图
dst_img = np.zeros([800, 800, channels], np.uint8)
# 按比例等分
w_rate = float(w) / 800
h_rate = float(h) / 800

for c in range(channels):
    for dst_x in range(800):
        for dst_y in range(800):
            # 重合中心
            src_x = (dst_x + 0.5) * w_rate - 0.5
            src_y = (dst_y + 0.5) * h_rate - 0.5

            src_x0 = int(src_x)
            src_x1 = min(int(src_x + 1), w-1)
            src_y0 = int(src_y)
            src_y1 = min(int(src_y + 1), h-1)

            # 计算 与p点同一垂直线上的 r1，r2
            r1 = (src_x1 - src_x) * src_img[src_x0, src_y0, c] + (src_x - src_x0) * src_img[src_x1, src_y0, c]
            r2 = (src_x1 - src_x) * src_img[src_x0, src_y1, c] + (src_x - src_x0) * src_img[src_x1, src_y1, c]

            #  变化值y2*r1 + 变化值y1*r2
            dst_img[dst_x, dst_y, c] = int((src_y1 - src_y) * r1 + (src_y - src_y0) * r2)

cv2.imshow('bilinear', dst_img)
cv2.waitKey(0)