'''
Created on 6 Aug 2015

@author: Coryn
'''
import cv2
import scipy as sp
import numpy as np


height = 720
width = 1200
rows = 5
columns = 5
h = height / rows
w = width / columns

def resizeImages(images):
    numImg = len(images)
    
    
    imagesSmall = images
    
    cr = 0
    for row in images:
        cc = 0
        for image in row:
            #print cc, cr
            imageSmall = cv2.resize(image,(w,h))
            imagesSmall[cr][cc] = imageSmall
            cc = cc+1
        cr = cr + 1
        
  
        
    return imagesSmall
def showImages(images):
    numImg = len(images)
    
    
    dispImg = sp.zeros((height, width, 3), sp.uint8)
    
    imagesSmall = resizeImages(images)
    
    #print dispImg
    
    cr = 0
    for row in imagesSmall:
        cc = 0
        for imageS in row:
            sy = h * cc
            ey = sy + h
            sx = w * cr
            ex = sx + w
            dispImg[sy:ey,sx:ex,:] = imageS
            cc = cc+1
        cr = cr + 1
    
   # h1, w1 = img1.shape[:2]
   # h2, w2 = img2.shape[:2]
   # view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
   # view[:h1, :w1, 0] = img1
  #  view[:h2, w1:, 0] = img2
    #dispImg[:, :, 1] = dispImg[:, :, 0]
   # dispImg[:, :, 2] = dispImg[:, :, 0]
    
    cv2.imshow("image", dispImg)
    cv2.waitKey()
    
def main():
    rt = "F:/Coryn/Documents/Project_Images/Turner/N/N02/"
    i1 = cv2.imread(rt + "N02001_10.jpg")
    i2 = cv2.imread(rt + "N02002_10.jpg")
    i3 = cv2.imread(rt + "N02055_10.jpg")
    i4 = cv2.imread(rt + "N02064_10.jpg")
    imgs = [[i1,i2],[i3,i4]]
    imgsSmall = resizeImages(imgs)
    
    showImages(imgs)
    #imgsSmall = np.array(imgsSmall)