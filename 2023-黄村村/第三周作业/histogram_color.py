import cv2

img = cv2.imread('lenna.png',1)
b, g, r = cv2.split(img)
bh = cv2.equalizeHist(b)
gh = cv2.equalizeHist(g)
rh = cv2.equalizeHist(r)

dst = cv2.merge((bh, gh, rh))
cv2.imshow('', dst)
cv2.waitKeyEx(0)
# cv2.imwrite('./result_eq.jpg', dst)


