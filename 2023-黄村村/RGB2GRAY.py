import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray

# 读取原图，w, h
src_img = cv2.imread('lenna.png')
w, h, channels = src_img.shape
# 创建等大空白图
dst_img = np.zeros((w, h), src_img.dtype)
# 1、手动循环转gray
# 循环行列为每个像素赋值
for i in range(w):
    for j in range(h):
        m = src_img[i, j]
        dst_img[i, j] =  0.11*m[0] + 0.59*m[1] + 0.3*m[2]  # bgr
# 显示转gray后的图像
cv2.imshow('hand_gray', dst_img)
cv2.waitKey(0)

# 2.1、调用接口cv2
cv2_dst_img = cv2.cvtColor(src_img,cv2.COLOR_BGR2GRAY)
plt.imshow(cv2_dst_img, 'gray')
plt.show()

# 2.2 调用接口skimge
ski_dst_img = rgb2gray(src_img)
cv2.imshow('ski_gray',ski_dst_img)
cv2.waitKey(0)


# 二值化
ez_dst_img = np.zeros((w,h), src_img.dtype)
for i in range(w):
    for j in range(h):
        if dst_img[i, j]/255.0 < 0.5:
            ez_dst_img[i, j] = 0
        else:
            ez_dst_img[i, j] = 1
# cv2.imshow('hand2ez',dst_img)  # 如果想用cv2.imshow显示二值图该咋写
# cv2.waitKey(0)
plt.imshow(ez_dst_img,'gray')
plt.show()

#调skimg接口转的灰度图进行二值化
ez_ski_dst_img = np.zeros((w,h), src_img.dtype)
for i in range(w):
    for j in range(h):
        if cv2_dst_img[i, j] / 255.0 < 0.5:
            ez_ski_dst_img[i, j] = 0
        else:
            ez_ski_dst_img[i, j] = 1
plt.imshow(ez_ski_dst_img,'gray')
plt.show()


#调cv2接口转的灰度图进行二值化
ez_cv2_dst_img = np.zeros((w,h), src_img.dtype)
for i in range(w):
    for j in range(h):
        if cv2_dst_img[i, j] / 255.0 < 0.5:
            ez_cv2_dst_img[i, j] = 0
        else:
            ez_cv2_dst_img[i, j] = 1
plt.imshow(ez_cv2_dst_img,'gray')
plt.show()