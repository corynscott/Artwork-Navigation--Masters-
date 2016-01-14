'''
Created on 28 Jul 2015

@author: Coryn
'''
import cv2
import numpy as np

img = cv2.imread('F:/1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

surf = cv2.SURF(400)
surf.hessianThreshold = 2000

kp, des = surf.detectAndCompute(gray,None)
print len(des)
print des
img=cv2.drawKeypoints(gray,kp)
cv2.imwrite('F:/1surf.jpg',img)