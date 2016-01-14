'''
Created on 13 Aug 2015

@author: Coryn except for plot_raw_TSNE() which was adapted from cnnembed code written by Andrej Karpathy the source of which can be found at http://cs.stanford.edu/people/karpathy/cnnembed/
'''
import numpy as np
from util import util, dirm
import math
import cv2
from matplotlib import pyplot as plt  
from databasehandler import imagesHandler, tsneHandler
from cv2 import imread
import collections

# Plot the images based on nearest neighbours
#Coryn Adapted from cnnembed code included in project or avaliable from http://cs.stanford.edu/people/karpathy/cnnembed/
def plot_raw_TSNE(tsneValues,imageIDs,filename):
    print "Plotting " +filename
    filename = filename + "_raw"
    locations = [] #loc keeps track of where the images are being placed in the visualisation
    
    #Load Tsne Values 
    x = np.array(tsneValues)
    
    #subtract the min of each column
    x = x - x.min(axis=0)
    #devide by the max of each column
    x = x / x.max(axis=0)
    
    #get filename
    fs = imageIDs
    N = len(fs) #N = length(fs);
    
    
    # size of every individual image
    s = 250
    
    # size of final image
    S=10004
    
    # the final images intitialised
    G = np.ones((S,S,3)) # ,'uint8'
    G = G*255
    
    for i in range(0,N):
        a = math.ceil(x[i,0] * (S-s)+1)
        b = math.ceil(x[i,1] * (S-s)+1)
        a = a - ((a-1)%s)+1
        b = b - ((b-1)%s)+1
        #print meta,b
        imgid = fs[i].rstrip('\n')
        if i%100==0:
            print i,"/",len(fs) 
        if i==N:
            print i,"/",len(fs)
        img = imagesHandler.get_image(imgid)
        #CROPING
        #img_crop = util.cropImage(img,100,100)
        imgr = cv2.resize(img, (s, s))
        c=a+s
        #print c
        d=b+s
        G[a:c, b:d, :] = imgr;
        loc = [imgid,a,c,b,d]
        locations.append(loc)
    
    
    print "Saving Image:" + dirm.outputDirectory + filename + ".jpg"
    cv2.imwrite(dirm.outputDirectory + filename + ".jpg", G )
    print "Image Saved"
    tsneHandler.storeLoc(filename, locations)
    return G

# code 
# display the image
def displayImage(img):
    print "displaying image"
    plt.imshow(img)
    plt.show()

def displayInteractiveImage(img,name):
    ax = plt.gca()
    fig = plt.gcf()
    implot = ax.imshow(img)
    
    def onclick(event):
        if event.xdata != None and event.ydata != None:
            print(event.xdata, event.ydata)
            print lookupImage(event.xdata, event.ydata, name)
            print lookupImage(event.ydata, event.xdata, name)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    plt.show()

def lookupImage(x,y,name):
    locations = tsneHandler.getLoc(name)
    for loc in locations:
        id = loc[0]
        a =loc[1]
        c =loc[2]
        b =loc[3]
        d =loc[4]
        if x>b and x<d and y>a and y<c:
            return id
    return None    


def lookup_image_by_id(id_q,name):
    locations = tsneHandler.getLoc(name)
    for loc in locations:
        id = loc[0]
        a =loc[1]
        c =loc[2]
        b =loc[3]
        d =loc[4]
        if id==id_q:
            print a,b,c,d
    return None    

    
