'''
Created on 13 Aug 2015

@author: Coryn
'''
import numpy as np
import dirm
import csv


def loadCSV(filename):
    print "Importing:",filename
    f = open(dirm.outputDirectory + filename+".csv")
    #file.readline()  # skip the header
    data = np.loadtxt(f, delimiter = ',')
    print 'Importing Complete:',filename
    return data

def importCSV(filelocation):
    print "Importing:",filelocation
    f = open(filelocation)
    #file.readline()  # skip the header
    data = np.genfromtxt(f, dtype=None, delimiter=',')
    print 'Importing Complete:',filelocation
    return data

def loadText(filename):
    with open(dirm.outputDirectory + filename + ".txt") as f:
        content = f.readlines()
    return content

def writetoCSV(array,filename):
    print 'writing data to:',filename, ' dir:', dirm.outputDirectory
    with open(dirm.outputDirectory +filename +".csv", "wb") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(array)
    
def cropImage(img,x,y):
    height = img.shape[0]
    width = img.shape[1]
    
    crop_img = img[y:height-y,x:width-x]
    return crop_img
    
