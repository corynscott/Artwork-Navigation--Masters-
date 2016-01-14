'''
Created on 28 Jul 2015

@author: Coryn
'''
import cv2
import numpy as np
print cv2.__version__
from matplotlib import pyplot as plt

img1 = cv2.imread('F:/2.jpg')
gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

img2 = cv2.imread('F:/3.jpg')
gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

surf = cv2.SURF(400)
surf.hessianThreshold = 2000


kp1, des1 = surf.detectAndCompute(gray1,None)
kp2, des2 = surf.detectAndCompute(gray2,None)

# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

# Match descriptors.
matches = bf.match(des1,des2)

# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)


# Draw first 10 matches.
#img3 = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS(img1,kp1,img2,kp2,matches[:10])
img3=cv2.drawKeypoints(gray1,matches[:10])
cv2.imwrite('F:/2mat.jpg',img3)

img4=cv2.drawKeypoints(gray2,matches[:10])
cv2.imwrite('F:/3mat.jpg',img4)
