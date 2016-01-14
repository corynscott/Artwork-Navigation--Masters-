'''
Created on 22 Aug 2015

@author: Coryn
'''
from sklearn import metrics
import cv2
from util import dirm
import numpy as np
labels_true = [1,1,1,1]
labels_pred= [1,1,2,1]
#print metrics.v_measure_score(labels_true, labels_pred))
S=200
G = np.zeros((S,S,3)) # ,'uint8
H = np.ones((S,S,3))
H = H *255
cv2.imshow("",H)
cv2.imwrite(dirm.outputDirectory + "testWhite"+ ".jpg", H )
cv2.waitKey()