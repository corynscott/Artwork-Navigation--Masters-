'''
Created on 29 Aug 2015

@author: Coryn
'''
from meta.metabo import metabagofwords
from sklearn.cluster.k_means_ import KMeans
import numpy as np
from databasehandler import imagesHandler, colourHandler, hogHandler,\
    sift_cb_handler, orb_cb_handler
from databasehandler import surf_cb_handler
from dynd.tests.test_computed_fields import scipy
from sklearn import metrics
from time import time
from sklearn.preprocessing.data import normalize
from util import util
from metadata_analysis import associate_cluster
from collections import Counter


np.set_printoptions(threshold=np.nan)

def performKmeans(data,n_clusters):
    
    print "Performing K-Means on data"
    est = KMeans(n_clusters)
    est.fit(data)
    labels = est.labels_
    labels_np = np.array(labels)
    
    return labels,est


def bench_k_means(labels,sample_size,estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('% 9s   %.2fs    %i   %.3f   %.3f   %.3f   %.3f   %.3f    %.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))
    




import numpy
numpy.set_printoptions(threshold=numpy.nan)
names_vec = metabagofwords()
content_labels, content_est =[],[]
sample_size = len(content_labels)

dates_clustered, mediums_clustered = associate_cluster.assignclustertoallimages()
print dates_clustered, len(dates_clustered)
print mediums_clustered, len(mediums_clustered)
print content_labels, len(content_labels)

rgb_data = colourHandler.getColourDistForAllImages("RGB")
rgb_data = np.array(rgb_data,dtype=None)
rgb_data= np.delete(rgb_data,0,1)

lab_data = colourHandler.getColourDistForAllImages("LAB")
lab_data = np.array(lab_data,dtype=None)
lab_data= np.delete(lab_data,0,1)

gistVals = util.loadCSV("gistvals")
gist_data = np.array(gistVals)

#hogHandler.extract_hog_from_all_images()
hog_data = hogHandler.getHogValsforAllImages()
hog_data = np.array(hog_data,dtype=None)
hog_data= np.delete(hog_data,0,1)
hog_data = np.array(hog_data)

#surfCodebook.run_codebook(n_clusters,400, 0.3, cv2.INTER_CUBIC, 0)
surf_data = surf_cb_handler.get_distributions()
surf_data = np.array(surf_data,dtype=None)
surf_data= np.delete(surf_data,0,1)

sift_data = sift_cb_handler.get_distributions()
sift_data = np.array(sift_data,dtype=None)
sift_data= np.delete(sift_data,0,1)

orb_data = orb_cb_handler.get_distributions()
orb_data = np.array(orb_data,dtype=None)
orb_data= np.delete(orb_data,0,1)


def perLabel(label_name,labels,sample_size,n_clusters):
    print(79 * '_')
    print label_name
    print('% 9s' % 'feature'
          '    time  inertia    homo   compl  v-meas     ARI AMI  silhouette')
    #print "number of distinct classes for true labels for ",label_name, len(Counter(labels))
    estimator = KMeans(n_clusters=n_clusters)
    bench_k_means(labels,sample_size,estimator, "RGB", rgb_data)
    bench_k_means(labels,sample_size,estimator, "LAB", lab_data)
    bench_k_means(labels,sample_size,estimator, "HOG", hog_data)
    bench_k_means(labels,sample_size,estimator, "GIST", gist_data)
    bench_k_means(labels,sample_size,estimator, "SURF", surf_data)
    bench_k_means(labels,sample_size,estimator, "SIFT", sift_data)
    bench_k_means(labels,sample_size,estimator, "ORB", orb_data)
    
    
    
def run():
    sample_size = 1241

    n_clusters = 30
    content_labels, content_est = performKmeans(names_vec, n_clusters) 
    perLabel("content", content_labels, sample_size, n_clusters) 
    
    #n_clusters = len(Counter(mediums_clustered))
    content_labels, content_est = performKmeans(names_vec, n_clusters) 
    perLabel("Medium", mediums_clustered, len(mediums_clustered), n_clusters)

   # n_clusters = len(Counter(dates_clustered))
    content_labels, content_est = performKmeans(names_vec, n_clusters) 
    perLabel("dates", dates_clustered, len(dates_clustered), n_clusters)


run()

def perform():
    #imagesHandler.load_images()
    #colourHandler.extract_colour_distribution_from_all_images("RGB")
    RGB_data = colourHandler.getColourDistForAllImages("RGB")
    RGB_data = np.array(RGB_data,dtype=None)
    RGB_data= np.delete(RGB_data,0,1)
    
    LAB_data = colourHandler.getColourDistForAllImages("LAB")
    LAB_data = np.array(RGB_data,dtype=None)
    LAB_data= np.delete(RGB_data,0,1)
    
    gistVals = util.loadCSV("gistvals")
    gist_data = np.array(gistVals)
    
    #hogHandler.extract_hog_from_all_images()
    hog_data = hogHandler.getHogValsforAllImages()
    hog_data = np.array(hog_data,dtype=None)
    hog_data= np.delete(hog_data,0,1)
    hog_data = np.array(hog_data)
    
    #surfCodebook.run_codebook(n_clusters,400, 0.3, cv2.INTER_CUBIC, 0)
    surf_data = surf_cb_handler.get_distributions()
    surf_data = np.array(surf_data,dtype=None)
    surf_data= np.delete(surf_data,0,1)
    
    sift_data = sift_cb_handler.get_distributions()
    sift_data = np.array(sift_data,dtype=None)
    sift_data= np.delete(sift_data,0,1)
    
    orb_data = orb_cb_handler.get_distributions()
    orb_data = np.array(surf_data,dtype=None)
    orb_data= np.delete(surf_data,0,1)
    
    
    
    
    est = KMeans(n_clusters=30)
    
    print(79 * '_')
    print('% 9s' % 'init'
          '    time  inertia    homo   compl  v-meas     ARI AMI  silhouette')
    
    bench_k_means(est, "colourPerfomanceVmeta", colour_data)
    bench_k_means(est, "hogPerfomanceVmeta", hog_data)
    #bench_k_means(est, "surfPerfomanceVmeta", surf_data)