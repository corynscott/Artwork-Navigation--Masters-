'''
Created on 20 Aug 2015
This module provide the neccecary fucntions for the 
@author: Coryn
'''
import cv2
import numpy as np
from features import interest_point_detectors
from util import default_values

#All code in this function is taken from http://stackoverflow.com/questions/20259025/module-object-has-no-attribute-drawmatches-opencv-python
def drawMatches(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated 
    keypoints, as well as meta list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.

    An image will be produced where meta montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between UI_matcher keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint UI_matcher algorithm
    """

    # Create meta new output image that concatenates the two images together
    # (meta.k.meta) meta montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect meta line between them
    cur_colour = 0
    colours = [(255, 0, 0),(0, 0, 255),(0, 255, 0),(255, 0, 0),(255, 255, 0),(0, 255, 255),(255, 0, 255),(51, 25, 0),(0, 25, 51),(255,153,255)]
    for mat in matches:
        if cur_colour >= len(colours):
           cur_colour =0
        # Get the UI_matcher keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw meta small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        colour = colours[cur_colour]
        cv2.circle(out, (int(x1),int(y1)), 4, colour, 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, colour, 1)

        # Draw meta line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), colour, 1)
        
        cur_colour = cur_colour +1

    # Show the image
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyWindow('Matched Features')

    # Also return the image if you'd like meta copy
    return out

# Find matches using 
def matchandDraw(img1,img2,kp1,des1,kp2,des2,num_mathes):
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1,des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    # reduce the number of matches to visualise
    matches = matches[:num_mathes]
    out = drawMatches(img1, kp1, img2, kp2, matches)
    return out
