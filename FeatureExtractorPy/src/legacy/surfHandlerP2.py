'''
Created on 5 Jul 2015
!!!WHY ARE WE SHORT TWO COLUMNS
@author: Coryn
'''
import sqlite3
from util import dirm
import os
from features import surf
import cv2
import cPickle

table_name = "table1"


def createDatabaseTable():
    cmd = 'CREATE TABLE {tn} (data BLOB)'.format(tn=table_name)
    print cmd
    c.execute(cmd)

       
def dropDatabaseTable():
    cmd = 'DROP TABLE IF EXISTS {tn}'.format(tn=table_name)
    print cmd
    c.execute(cmd)

def processSurf(img,imageId):

    data = 325
    pdata = cPickle.dumps(data, cPickle.HIGHEST_PROTOCOL)
    pdatabin = sqlite3.Binary(pdata)
    kpDes, numDescriptors = surf.calc_surf_blend(img)
    kpDes_pickle = cPickle.dumps(kpDes, cPickle.HIGHEST_PROTOCOL)
    kpDes_bin = sqlite3.Binary(kpDes_pickle)
    print cPickle.HIGHEST_PROTOCOL
    print pdata
    print pdatabin
    c.execute("""INSERT INTO table1 (data) VALUES (?)""",(kpDes_bin,))
        
def processSurfAllImages():
   
    c.execute('SELECT * FROM images')
    images =c.fetchall()
    #print images
    numimg = 0
    for image in images:
        if numimg%1==0:
                print numimg
        imageId = image[0]
        imageURL = image[1]
        img = cv2.imread(dirm.rootDirectory + imageURL)
        processSurf(img,imageId)
        numimg = numimg +1
        
        
        
def find():
    
        cmd = 'SELECT imageId from images WHERE imageId = N00369'
        #cmd = 'SELECT imageId from images WHERE imageId={iId}'.format(iId='N00369',)
        print cmd
        store = c.execute(cmd)
        print store 
    
conn = sqlite3.connect(dirm.sqlite_file)
c = conn.cursor()


dropDatabaseTable()
createDatabaseTable()
#processSurfAllImages()
img = cv2.imread('F:/2.jpg')
processSurf(img, 'N00369')
#filename = 'dog'
#c.execute('PRAGMA foreign_keys = ON;')

conn.commit()
conn.close()
    