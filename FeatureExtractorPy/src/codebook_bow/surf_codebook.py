'''
Created on 7 Aug 2015

@author: Coryn
'''
import cv2
from util import dirm
from features import interest_point_detectors
import numpy as np
from sklearn.cluster.k_means_ import KMeans
from databasehandler import imagesHandler
from databasehandler import surf_cb_handler
     
def extract_all_descriptors(hessian_threshold,resize_ratio, resize_method, crop_amount):
    print 'Extracting Discriptors: SURF'
    images = imagesHandler.get_all_img_rows()
    concatDesc = []
    concatIds = []
    numimg = 0
    numDesc = 0
    for image in images:
        if numimg%100==0:
                print numimg
        imageId = image[0]
        imageURL = image[1]
        img = cv2.imread(dirm.rootDirectory + imageURL)
        try:
            kp,desc,gray = interest_point_detectors.calculate_surf_values(img, hessian_threshold, resize_ratio, resize_method, crop_amount)
            numDesc = numDesc + len(desc)
            for d in desc:
                concatDesc.append(d)
                concatIds.append([imageId,len(desc)])
       
        except Exception,e:
            print "unable to process image "+imageId
            print str(e)
        numimg = numimg +1
            
    surf_cb_handler.store_descriptors(concatDesc)
    return concatDesc

def performKmeans(data,n_clusters):
    
    print "Performing K-Means on data"
    est = KMeans(n_clusters)
    est.fit(data)
    surf_cb_handler.store_estimator(est)
    
    return est

def build_distribution(est, n_clusters, hessian_threshold, resize_ratio, resize_method, crop_amount):
    print 'BuildingDistribution'
    images = imagesHandler.get_all_img_rows()
    allDist = []
    numimg = 0
    for image in images:
        if numimg%100==0:
                print numimg
        imageId = image[0]
        imageURL = image[1]
        img = cv2.imread(dirm.rootDirectory + imageURL)
        
        #print dirm.rootDirectory + imageURL
        try:
            kp,desc,gray = interest_point_detectors.calculate_surf_values(img, hessian_threshold, resize_ratio, resize_method, crop_amount)
        except Exception,e:
            print "unable to process image "+imageId
            print str(e)
        
        dist =  np.zeros((n_clusters))
        imagePred = est.predict(desc)
        for p in imagePred:
            dist[p] = dist[p] + 1
        dist = dist / len(imagePred)
        allDist.append([imageId] + dist.tolist())
        numimg = numimg +1
        
    surf_cb_handler.store_distributions(allDist)
    
    
def run_codebook(n_clusters,hessian_threshold, resize_ratio, resize_method, crop_amount):
    surf_cb_handler.drop_database_table()
    surf_cb_handler.create_database_table()
    desc = extract_all_descriptors(hessian_threshold, resize_ratio, resize_method, crop_amount)
    est = performKmeans(desc,n_clusters)
    build_distribution(est, n_clusters, hessian_threshold, resize_ratio, resize_method, crop_amount)

