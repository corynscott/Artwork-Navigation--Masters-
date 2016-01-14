#!/usr/bin/env python
# using SURF semantic features

import pdb
import urllib
import os
import sys
import shutil
from ms_code_paginator import *
from scipy.cluster.vq import whiten
from scipy.cluster.vq import kmeans
from scipy.cluster.vq import vq
import Image
import numpy
import cv2 #OpenCV toolbox
from utils import lab
from kernelized_sorting_chisquared import KS

def search(query,n=40,start=0):
    # retrieve top n results of query
    # default is 40 results per page
    
    dict_res = BossImageIndex().CallBoss(query,n,start)
    im_res = dict_res['ysearchresponse']['resultset_images']
    res = []
    for i in xrange(n):
        res.append((im_res[i]['thumbnail_url'],i))
    
    #path_name = "/Library/WebServer/results/"+query
    path_name = "/Users/novi/my_image_search/results/"+query
    
    # create the folder (if does not exist) to save query results
    if os.path.isdir(path_name):
        shutil.rmtree(path_name)
        os.mkdir(path_name)
    else:
        os.mkdir(path_name)
    
    # download the image results
    image = urllib.URLopener()
    silentcounter = 1
    imagefile = []
    for counter in xrange(n):
        urltoberetrieved = res[counter][0]
        #print urltoberetrieved
        filename = '%s/%s.%s' % (path_name,silentcounter,'jpg')
        #try:
        image.retrieve(urltoberetrieved,filename)
        imagefile.append(filename)
        silentcounter = silentcounter + 1
        #except IOError:
        #    print 'error at %s \n' % (urltoberetrieved)
        #    pass
    
    # prepare the color image feature
    pref = numpy.array([[0,0]]) # [image #,position #]
    ldesc = []
    codes = 30 #number of k-means cluster
    ino = 5
    jno = 8 # default grid: 5 by 8 2D grid
    show = ino*jno
    lim = show
    
    silentcounter = 1
    for i_img in xrange(lim): 
        fname = imagefile[i_img]
        try:    
            im = cv.LoadImage(fname,0) # loading with OpenCV (gray chanel only)
            silentcounter = silentcounter + 1
        except:
            print 'image thumbnail can not be retrieved'
            sys.exit(0)
        
        #resizing the image
        #om = cv.CreateImage((psize,psize),im.depth,im.nChannels)
        #cv.Resize(im,om,cv.CV_INTER_CUBIC)
        storage = cv.CreateMemStorage(0)
        #generating the mask
        #mat = cv.CreateMat(psize,psize,cv.CV_8UC1)
        #extracting SURF feature
        #[keypoints,descriptors] = cv.ExtractSURF(om,mat,storage,(1,500,3,4))
        [keypoints,descriptors] = cv.ExtractSURF(im,im,storage,(1,500,3,4))
        ldesc.append(descriptors)        
    
    #perform vector quantization
    tarrdesc = [numpy.array(ldesc[i]) for i in range(show)]
    lendesc = [ldesc[i].__len__() for i in range(show)]
    arrdesc = numpy.concatenate([tarrdesc[i] for i in range(show)])
    arrdesc = whiten(arrdesc)
    [codebook,distortion] = kmeans(arrdesc,codes)
    [code,dist] = vq(arrdesc,codebook)
    
    #generate the semantic feature
    imgdata = numpy.zeros((show,codebook.shape[0]),dtype=float)
    code_offset = 0
    for i_img in xrange(show):
        code_index = range(code_offset,code_offset+lendesc[i_img])
        for i_code in code_index:
            imgdata[i_img,code[i_code]] = imgdata[i_img,code[i_code]]+1
        code_offset = code_offset + lendesc[i_img]
        
    #normalize the semantic feature
    sumimgdata = numpy.sum(imgdata,axis=1)
    sumimgdata.shape = show,1
    imgdata = imgdata/sumimgdata
    
    griddata = numpy.zeros((2,ino*jno))
    griddata[0,] = numpy.kron(range(1,ino+1),numpy.ones((1,jno)))
    griddata[1,] = numpy.tile(range(1,jno+1),(1,ino))
    
    # do kernelized sorting procedure
    PI = KS(imgdata,griddata.T,pref)
    i_sorting = PI.argmax(axis=1)
    
    #creating the passed dictionary
    sorted_dict_res = {}
    sorted_dict_res['count'] = dict_res['ysearchresponse']['count']
    sorted_dict_res['totalhits'] = dict_res['ysearchresponse']['totalhits']
    sorted_dict_res['start'] = dict_res['ysearchresponse']['start']
    sorted_dict_res['resultset_images'] = [dict_res['ysearchresponse']['resultset_images'][i] for i in i_sorting]
    return sorted_dict_res