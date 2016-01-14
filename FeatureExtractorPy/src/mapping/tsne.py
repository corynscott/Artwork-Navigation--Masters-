'''
Created on 16 Jul 2015

@author: Coryn
'''
from sklearn.manifold.t_sne import TSNE
import sqlite3
from util import dirm
from databasehandler import tsneHandler, imagesHandler, sift_cb_handler
from databasehandler import surf_cb_handler
from databasehandler import orb_cb_handler
import numpy as np
import cv2
from mapping import plot_visualisation
from util import util

#Calculates tsne and stores it in tsne database for colour and hog takes the table names as parameter
def TSNE_General(tablename):
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
    model = TSNE(n_components=2, random_state=0)
    tsne_vals = model.fit_transform(X)
    tsneHandler.storeTsneValsWIds(tablename, tsne_vals, ids)
    return tsne_vals,ids


#Calculates tsne and stores it in tsne database for surf takes the name to store under as param
def TSNE_Surf(name):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    dist = surf_cb_handler.get_distributions()
    X_Ids = []
    X_data = []
    for d in dist:
        x_id = d[0]
        x_data = d[1:]
        X_Ids.append(x_id)
        X_data.append(x_data)
    X_data  = np.array(X_data)
    model = TSNE(n_components=2)
    tsne_x = model.fit_transform(X_data)
    tsneHandler.storeTsneValsWIds(name, tsne_x, X_Ids)
    return tsne_x,X_Ids

#Calculates tsne and stores it in tsne database for orb takes the name to store under as param

def TSNE_orb(name):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    dist = orb_cb_handler.get_distributions()
    X_Ids = []
    X_data = []
    for d in dist:
        x_id = d[0]
        x_data = d[1:]
        X_Ids.append(x_id)
        X_data.append(x_data)
    X_data  = np.array(X_data)
    model = TSNE(n_components=2)
    tsne_x = model.fit_transform(X_data)
    tsneHandler.storeTsneValsWIds(name, tsne_x, X_Ids)
    return tsne_x,X_Ids
 
 #Calculates tsne and stores it in tsne database for sift takes the name to store under as param
def TSNE_sift(name):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    dist = sift_cb_handler.get_distributions()
    X_Ids = []
    X_data = []
    for d in dist:
        x_id = d[0]
        x_data = d[1:]
        X_Ids.append(x_id)
        X_data.append(x_data)
    X_data  = np.array(X_data)
    model = TSNE(n_components=2)
    tsne_x = model.fit_transform(X_data)
    tsneHandler.storeTsneValsWIds(name, tsne_x, X_Ids)
    return tsne_x,X_Ids

#Calculates tsne and stores it in tsne database for gist takes the name to store under as param
def TSNE_Gist(name,csvfilename):
    idsT = imagesHandler.get_all_img_ids()
    ids = []
    for id in idsT:
        ids.append(str(id[0]))
    print ids
    gistVals = util.loadCSV(csvfilename)
    X = np.array(gistVals)
    model = TSNE(n_components=2, random_state=0)
    tsne_vals = model.fit_transform(X)
    tsneHandler.storeTsneValsWIds(name, tsne_vals, ids)
    return tsne_vals,ids

def main():
    filenm = "surf3"   
    #tsne_x,X_Ids = TSNE_Surf(filenm)
    Tsne,ids = tsneHandler.getTSNEwithIds(filenm)
    img = plot_visualisation.plot_raw_TSNE(Tsne, ids, filenm)
    #img = cv2.imread(dirm.outputDirectory+"surf3.jpg")
    plot_visualisation.displayInteractiveImage(img, "surf3")
    
