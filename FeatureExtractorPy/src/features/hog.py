'''
Created on 2 July 2015
# This module provides the functions to extract the Histogram of Oriented Gradients for a given image
@author: Coryn in conjunction with OpenCV tutorial found at http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_ml/py_svm/py_svm_opencv/py_svm_opencv.html
        And the scikit-image documentation
        
'''
import cv2
import numpy as np
from util import dirm

from skimage.feature import hog
from skimage import color,exposure
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import timeit
from matplotlib.cm import get_cmap

#number of bins per sub-square
bin_n = 16

# Code taken/adapted from http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_ml/py_svm/py_svm_opencv/py_svm_opencv.html
# calculate the Histogram of Oriented Gradients for the specified image (param)
def calc_hog(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  # convert the image to gray-scale
    gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)   # extract the gradient information in the x-axis
    gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)   # extract the gradient information in the x-axis
    mag, ang = cv2.cartToPolar(gx, gy)  # convert the gradient information into magnitude and direction (angle)
    
    bins = np.int32(bin_n*ang/(2*np.pi))    # quantising bin values in (0...16)
    
    # Divide the image into 4 sub-squares, cacluate the magnitude 
    bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
    mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)
    return hist

# extract the Histogram of Oriented Gradients for the specified image found at the image_url (param)
def extract_hog_histogram(image_url):
    img = cv2.imread(dirm.rootDirectory + image_url)
    hist = calc_hog(img)
    return hist

# code to calcualte the HOG using the scikit-image library
# code adapted from http://scikit-image.org/docs/dev/auto_examples/plot_hog.html
def calc_hog_scikit(img):
    grey = color.rgb2gray(img)
    fd = hog(grey, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualise=False)
    return fd

# plot the hog feature using sckit-image library
# code from http://scikit-image.org/docs/dev/auto_examples/plot_hog.html
def plot_hog_scikit(img):
    grey = color.rgb2gray(img)
    fd, hog_image= hog(grey, orientations=8, pixels_per_cell=(16, 16),
                    cells_per_block=(1, 1), visualise=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
    
    ax1.axis('off')
    ax1.imshow(grey, cmap = get_cmap("gray"))
    ax1.set_title('Input image')
    
    # Rescale histogram for better display
    hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))
    
    ax2.axis('off')
    ax2.imshow(hog_image_rescaled, cmap = get_cmap("gray"))
    ax2.set_title('Histogram of Oriented Gradients')
    plt.show()
    
    
# Compare the running times of the OpenCV implemented version and the scikit-image implementation
def comparerunningtimes(img):
    start = timeit.default_timer()
    fd= calc_hog_scikit(img)
    stop = timeit.default_timer()
    print "skimage", stop-start
    
    start = timeit.default_timer()
    calc_hog(img)
    stop = timeit.default_timer()
    print "cv2:", stop-start
    
#img = cv2.imread("f:/1.jpg")
#plot_hog_scikit(img)