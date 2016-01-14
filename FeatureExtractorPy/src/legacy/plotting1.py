'''
Created on 13 Aug 2015

@author: Coryn
'''
import numpy as np
from util import util
import math
import cv2
from databasehandler import tsneHandler

def plotCompTSNE(tsneValues,imageIDs,filename):
    print "Plotting " +filename
    filename = filename + "_raw"
    locations = []
    x = np.array(tsneValues)
    #subtract the min of each column
    x = x - x.min(axis=0)
    #devide by the max of each column
    x = x / x.max(axis=0)
    
    #get filename
    fs = imageIDs
    N = len(fs) #N = length(fs);
    
    #size of final image
    S = 10008;
    G = np.zeros((S,S,3)) # ,'uint8'
    #print G
    # size of every image thumbnail
    s = 278
    
    
    xnum = S/s
    ynum = S/s
    used = np.zeros((N, 1))
    
    qq=len(range(0,S,s))
    
    abes = np.zeros((qq*2,2))
    print len(abes)

    i=0
    for a in range(0,S,s):
        for b in range(0,S,s):
            abes[i,:] = [a,b]
            i=i+1;
    print abes


tsne_vals,ids = tsneHandler.getTSNEwithIds("colourDistribution")
plotCompTSNE(tsne_vals, ids, "colourPlot")