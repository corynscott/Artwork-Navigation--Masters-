'''
Created on 28 Jul 2015

@author: Coryn
'''
import cv2
import numpy as np
from util import dirm
print cv2.__version__
from matplotlib import pyplot as plt
import cPickle as pickle

def pickle_keypoints(keypoints, descriptors): 
    i = 0 
    temp_array = [] 
    for point in keypoints: 
        temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, descriptors[i])
        i+=1 
        temp_array.append(temp)
    return temp_array 

def unpickle_keypoints(array):
    keypoints = [] 
    descriptors = [] 
    for point in array:
        temp_feature = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5]) 
        temp_descriptor = point[6] 
        keypoints.append(temp_feature) 
        descriptors.append(temp_descriptor) 
    return keypoints, np.array(descriptors)

def store(kp,des):
    try:
        temp_array = pickle.load( open( dirm.outputDirectory+"keypoints_database.p", "rb" ) )
    except Exception,e:
        temp_array = []
     
    temp = pickle_keypoints(kp1, des) 
    temp_array.append(temp) 
    pickle.dump(temp_array, open(dirm.outputDirectory+"keypoints_database.p", "wb"))
    

def load(sid):
    keypoints_database = pickle.load( open(dirm.outputDirectory+"keypoints_database.p", "rb" ) )
    kp, des = unpickle_keypoints(keypoints_database[sid]) 
    return kp,des

img1 = cv2.imread('F:/2.jpg')
gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

img2 = cv2.imread('F:/3.jpg')
gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

surf = cv2.SURF(400)
surf.hessianThreshold = 100


kp, des = surf.detectAndCompute(gray1,None)
print len(kp)
kpdes = pickle_keypoints(kp,des)
pdata = pickle.dumps(kpdes, pickle.HIGHEST_PROTOCOL)
data = pickle.loads(pdata)
print len(pdata)

kp1,des1 = unpickle_keypoints(data)
print kp[1].pt
print kp1[1].pt
#print kp1
#print kp1p
#print kp1up

#store(kp1,des1)
#store(kp2,des2)


#kp1R, des1R = load(0)
#kp2R, des2R = load(1)


#print kp1 == kp1R

