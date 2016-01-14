'''
Created on 28 Jun 2015
Code adapted from http://www.pyimagesearch.com/2014/01/22/clever-girl-meta-guide-to-utilizing-color-histograms-for-computer-vision-and-image-search-engines/
@author: Coryn
'''
import numpy as np
import cv2
from util import dirm

num_bins = 192

# calculate the colour histogram in rgb colour space for the given image passed as a parameter
def calc_hist_rgb(img):
    chans = cv2.split(img)  # convert to image channels
    num_chans = 3
    num_bins_per_channel = num_bins / num_chans 
    image_histogram = ''
    #process each image channel
    for (chan) in chans:
        # create meta histogram for the current channel and
        # concatenate the resulting histograms for each
        # channel
        channel_histogram = cv2.calcHist([chan], [0], None, [num_bins_per_channel], [0, 256])
        channel_histogram = channel_histogram / img.size  # divide by the number of pixels in the image
      
        cv2.normalize(channel_histogram,channel_histogram,0,num_bins_per_channel,cv2.NORM_MINMAX)    # normalise the histogram
        
        channel_histogram = np.int32(np.around(channel_histogram)) # round the individual bins
        image_histogram = image_histogram + str(channel_histogram.tolist())  #add the channel histogram to the complete histogram
        
    return image_histogram

# extract the colour histogram in rgb colour space for the image_url passed as a parameter
def extract_colour_hist_rgb(image_url):
    img = cv2.imread(dirm.rootDirectory + image_url)
    return calc_hist_rgb(img)


# calculate the colour histogram in LAB colour space for the image passed as a parameter
def calc_hist_lab(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)    # convert image to lab colour space
    chans = cv2.split(img)  # convert to image channels
    num_chans = 3
    num_bins_per_channel = num_bins / num_chans
    image_histogram = ''
    
    # loop over the image channels
    for chan in chans:
        # create meta histogram for the current channel and
        # concatenate the resulting histograms for each
        # channel
        channel_histogram = cv2.calcHist([chan], [0], None, [num_bins_per_channel], [0, 256])
        
        channel_histogram = channel_histogram / img.size  # divide by the number of pixels in the image
        
        cv2.normalize(channel_histogram,channel_histogram,0,num_bins_per_channel,cv2.NORM_MINMAX)    # normalise the histogram
        
        channel_histogram = np.int32(np.around(channel_histogram)) # round the individual bins
        
        image_histogram = image_histogram + str(channel_histogram.tolist())   #add the channel histogram to the complete histogram
        
    return image_histogram

# extract the colour histogram in LAB colour space for the image_url passed as a parameter
def extract_colour_dist_lab(image_url):
    img = cv2.imread(dirm.rootDirectory + image_url)    # import the image with the image url (param)
    return calc_hist_lab(img)

# draw the colour histogram
def draw_hist(hist):
    h = np.zeros((300,num_bins,3))
    for x,y in enumerate(hist):
        cv2.line(h,(x,0),(x,y),(255,255,255))
    y = np.flipud(h)
    cv2.imshow("hist",y)
    cv2.waitKey()

    
#hist = extract_colour_dist_lab("f:/1.jpg")
#draw_hist(hist)