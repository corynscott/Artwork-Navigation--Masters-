'''
Created on 23 Aug 2015

@author: Coryn
'''
import numpy as np
from sklearn.cluster import KMeans
import sqlite3
from util import dirm, util
from databasehandler import tsneHandler

def Kmenas_General(tablename):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'SELECT * FROM {tn}'.format(tn=tablename)
    c.execute(cmd)
    all_rows = c.fetchall()
    ids = []
    data = []
    for row in all_rows:
        ids.append(str(row[0]))
        data.append(row[1:])
    X = np.array(data)
    
    estimators = {'k_means_3': KMeans(n_clusters=3),'k_means_5':KMeans(n_clusters=3),'k_means_8': KMeans(n_clusters=8)}

    est = KMeans(n_clusters=3)
    est.fit(X)
    labels = est.labels_
    labels_np = np.array(labels)
    results = []
    tsne_vals,ids2 = tsneHandler.getTSNEwithIds(tablename)
    tsne_x,tsne_y = zip(*tsne_vals)
    results = zip(ids,ids2,tsne_x,tsne_y,labels_np)
    #header = ('id','id2','tsne_x','tsne_y','lables')
    #results_w_header = header + results
    #print results_w_header
    util.writetoCSV(results, tablename + "_clustered")
    
#Kmenas_General("colourDistribution")

