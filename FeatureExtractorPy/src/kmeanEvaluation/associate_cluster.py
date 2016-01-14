'''
Created on 22 Aug 2015

@author: Coryn
'''
from util import util
from databasehandler import imagesHandler
from collections import Counter


date_clusters = [[1800,1820],[1821,1829],[1830,1831],[1832,1839],[1840,1850]]
medium_clusters = ['Watercolour on','Gouache and watercolour','Graphite', 'Watercolour','Gouache', 'Chalk', 'oil','crayon']
medium_clusters = [c.lower() for c in medium_clusters]

def checkDateCluster(date):
    date = float(date)
    for i in range(0,len(date_clusters)):
        start = date_clusters[i][0]
        end = date_clusters[i][1]
        #print date,start,date>=start,end,date<=end
        if date>=start and date<=end:
            return i
            
    print "cound not fit in date range", date, start,end
    return None
        
def checkMediumCluster(medium):
    medium = str(medium)
    for i in range(0,8):
        mediumcluster = medium_clusters[i]
        medium = str(medium)
        medium = medium.lower()
        if medium.startswith(mediumcluster):
            return i
        
    return 10
    print "cound assign cluster", medium
        
def assignclustertoallimages():
    filelocation = "F:/Coryn/Google Drive/Project/Image Collection/Tate/turner-meta.csv"
    
    images_meta_all = util.importCSV(filelocation)
    curImagesInDB = imagesHandler.get_all_img_ids_string()
    
    cur_img_meta = []
    for image in images_meta_all:
        id = image[0]
        if id in curImagesInDB:
            cur_img_meta.append(image)
    
    print len(cur_img_meta)
    
    ids = []
    titles =[]
    mediums =[] 
    mediums_clustered =[] 
    dates = []
    dates_clustered = []
    
    for image in cur_img_meta:
       
        id = image[0]
        title = image[1]
        medium = image[2]
        date = image[3]
        
        ids.append(id)
        titles.append(title)
        mediums.append(medium)
        mediums_clustered.append(checkMediumCluster(medium))
        dates.append(date)
        dates_clustered.append(checkDateCluster(date))
        
    return dates_clustered, mediums_clustered

def main():
    
    import numpy
    numpy.set_printoptions(threshold=numpy.nan)
    dates_clustered, mediums_clustered = assignclustertoallimages()
    print dates_clustered
    print mediums_clustered
    print Counter(dates_clustered)
    print len(Counter(dates_clustered))