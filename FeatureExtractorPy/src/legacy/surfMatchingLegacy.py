'''
Created on 20 Aug 2015

@author: Coryn
'''
import cv2
import numpy as np
from features import intrest_point_detectors
from util import default_values

def blend_keypoints(keypoints, descriptors): 
    i = 0 
    temp_array = [] 
    for point in keypoints: 
        temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, descriptors[i])
        i+=1 
        temp_array.append(temp)
    return temp_array 

def unblend_keypoints(array):
    keypoints = [] 
    descriptors = [] 
    for point in array:
        temp_feature = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5]) 
        temp_descriptor = point[6] 
        keypoints.append(temp_feature) 
        descriptors.append(temp_descriptor) 
    return keypoints, np.array(descriptors)

def matchesToArray(matches): 
    i = 0 
    temp_array = [] 
    totalDistance = 0
    for match in matches: 
        temp = (match.distance, match.trainIdx, match.queryIdx, match.imgIdx)
        totalDistance = totalDistance + match.distance
        i+=1 
        temp_array.append(temp)
    meanDistance = totalDistance / len(matches)
    return temp_array, meanDistance

def arrayToMatches(matches_array): 
    matches = []
    for match in matches_array:
        temp_match = cv2.DMatch(match[0],match[1],match[2],match[3])
        matches.append(temp_match)
    return matches    

def calc_surf_blend(img):
    
    kp, des = intrest_point_detectors.calculate_surf_values(img, hessian_threshold=default_values.hessian_threshold, resize_ratio=default_values.resize_ratio, resize_method=default_values.resize_method, crop_amount=default_values.crop_amount)
    numDescriptors = len(kp)
    kpDes = blend_keypoints(kp,des)
    return kpDes, numDescriptors

def bfMatch(kp1, des1,kp2, des2):
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1,des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    
   
    
    numMatches = len(matches)
    matches_array, meanDistance =  matchesToArray(matches)
    
    
#     matchesAboveThreashold = []
#     for m,n in matches:
#         if m.distance < 0.75*n.distance:
#             matchesAboveThreashold.append([m])
#    
    thres_dist = meanDistance * 0.75
    
    matchesAT = [m for m in matches if m.distance < thres_dist]
    
    #setMeanDistance to really high
    meanDistanceAT = 100000000
    matchesAT_array =[]
    if(len(matchesAT)>0):
        matchesAT_array, meanDistanceAT = matchesToArray(matchesAT)                         
             
    
    numMatchesAT = len(matchesAT)
    
    
    return matches_array,numMatches, meanDistance, matchesAT_array,numMatchesAT, meanDistanceAT 


def flannMatcher(kp1, des1,kp2, des2):

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    
    matches = flann.knnMatch(des1,des2,k=2)
   
    thres_distK = 0.75
    
    # store all the good matches as per Lowe's ratio test.
    matchesAT = []
    
    for m,n in matches:
        if m.distance < thres_distK*n.distance:
            matchesAT.append(m)
    
    
    
    #setMeanDistance to really high
    meanDistanceAT = 100000000
    matchesAT_array =[]
    if(len(matchesAT)>0):
        matchesAT_array, meanDistanceAT = matchesToArray(matchesAT)                         
             
    
    numMatchesAT = len(matchesAT)
    matches_array = []
    numMatches = 0
    meanDistance = 100000000000
    
    #print numMatches, meanDistance, numMatchesAT, meanDistanceAT 
    return matches_array,numMatches, meanDistance, matchesAT_array,numMatchesAT, meanDistanceAT 

    
   # return matches_array,numMatches, meanDistance, matchesAT_array,numMatchesAT, meanDistanceAT


#http://stackoverflow.com/questions/20259025/module-object-has-no-attribute-drawmatches-opencv-python
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
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
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
        # Get the matching keypoints for each of the images
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




def matchandDraw(img1,img2,kp1,des1,kp2,des2,num_mathes):
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1,des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    matches = matches[:num_mathes]
    out = drawMatches(img1, kp1, img2, kp2, matches)
    return out
