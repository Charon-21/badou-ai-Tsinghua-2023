import cv2
import matplotlib.pyplot as plt

src_img = cv2.imread('lenna.png')
gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

dst_img = cv2.equalizeHist(gray_img)


plt.imshow(gray_img, cmap='gray')
plt.show()

cv2.imshow('', dst_img)
cv2.waitKey(0)





