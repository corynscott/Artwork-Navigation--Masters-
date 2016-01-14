'''
Created on 15 July 2015, Refactored 12 August 2015
This module provides the functions to extract the keypoints and their respective descriptors, given an image.
@author: Coryn (all code in this module was developed by Coryn)
'''
import cv2
from util import image_managment

# take the image, the hassian_threshold, resize ratio (if 0, don't resize) and crop_amount (if 0, don't crop)
def calculate_surf_values(img,hessian_threshold,resize_ratio,resize_method,crop_amount):
    # crop if crop_amount above 0
    if crop_amount>0:
        img = image_managment.crop_image(img, crop_amount)
    
    # resize if resize ratio greater than 0
    if resize_ratio>0:
        img = image_managment.resize_image(img, ratio=resize_ratio, method=resize_method)
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convert image to gray-scale   
    surf = cv2.SURF()   # initialise our surf detector
    surf.hessianThreshold = hessian_threshold   # set the hessian threshold for our surf detector
    surf.extended = True    # use the 128 dimension descriptors
    kp, des = surf.detectAndCompute(gray,None)  # detect keypoints and compute descriptors
    return kp,des,gray


# take the image, resize ratio (if 0, don't resize) and crop_amount (if 0, don't crop)
def calculate_sift_values(img,resize_ratio,resize_method,crop_amount):
    # crop if crop_amount above 0
    if crop_amount>0:
        img = image_managment.crop_image(img, crop_amount)
    
    # resize if resize ratio greater than 0
    if resize_ratio>0:
        img = image_managment.resize_image(img, ratio=resize_ratio, method=resize_method)
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convert image to gray-scale   
    sift = cv2.SIFT()   # initialise our SIFT detector
    #sift.nfeatures = n_features # set the number of feature to retain
    kp, des = sift.detectAndCompute(gray,None)  # detect keypoints and compute descriptors
    return kp,des,gray

# take the image, resize ratio (if 0, don't resize) and crop_amount (if 0, don't crop)
def calculate_orb_values(img,resize_ratio,resize_method,crop_amount):
    # crop if crop_amount above 0
    if crop_amount>0:
        img = image_managment.crop_image(img, crop_amount)
    
    # resize if resize ratio greater than 0
    if resize_ratio>0:
        img = image_managment.resize_image(img, ratio=resize_ratio, method=resize_method)
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convert image to gray-scale   
    orb = cv2.ORB() # initialise our ORB detector
    kp,des = orb.detectAndCompute(gray,None)   # detect keypoints and compute descriptors
    return kp,des,gray

