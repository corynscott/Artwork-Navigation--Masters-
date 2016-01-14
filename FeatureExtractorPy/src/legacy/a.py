'''
Created on 18 Aug 2015

@author: Coryn
'''

import cv2

img = cv2.imread("f:/k.jpg")
height = img.shape[0]
width = img.shape[1]
print height,width
x = 100
y = 100

crop_img = img[y:height-y,x:width-x]
cv2.imshow("cropped",crop_img)
cv2.waitKey()

ratio = 0.3
img_resized = cv2.resize(img, None, None, ratio, ratio, cv2.INTER_CUBIC)