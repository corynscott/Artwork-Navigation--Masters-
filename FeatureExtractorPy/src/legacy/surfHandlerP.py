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
import cPickle as pickle
import cmd

table_name1 = "surf" + str(surf.hassianThreshold)
table_name = "surfAll" + str(surf.hassianThreshold)



def createDatabaseTable(c):
    cmd = 'CREATE TABLE {tn} (imageId TEXT PRIMARY KEY, numDescriptors INTEGER, descriptors BLOB , FOREIGN KEY(imageId) REFERENCES images(imageId))'.format(tn=table_name)
    print cmd
    c.execute(cmd)

       
def dropDatabaseTable(c):
    cmd = 'DROP TABLE IF EXISTS {tn}'.format(tn=table_name)
    print cmd
    c.execute(cmd)

def processSurf(img,imageId,c,conn):

    kpDes, numDescriptors = surf.calc_surf_blend(img)
    kpDes_pickle = pickle.dumps(kpDes, pickle.HIGHEST_PROTOCOL)
    kpDes_bin = sqlite3.Binary(kpDes_pickle)
    cmd = 'INSERT INTO {tn}(imageId, numDescriptors, descriptors) VALUES((SELECT imageId from images WHERE imageId="{iId}"), {numDes}, ?)'.format(tn=table_name,iId=imageId,numDes=numDescriptors)
    #print cmd   
    try:
        c.execute(cmd,(kpDes_bin,))
        conn.commit()
    except sqlite3.IntegrityError:
        print('ERROR: ID already exists in PRIMARY KEY column {}'.format(imageId))
                    
                
        
def processSurfAllImages(c,conn):
   
    c.execute('SELECT * FROM images')
    images =c.fetchall()
    #print images
    numimg = 0
    for image in images:
        if numimg%100==0:
                print numimg
        imageId = image[0]
        imageURL = image[1]
        img = cv2.imread(dirm.rootDirectory + imageURL)
        #print dirm.rootDirectory + imageURL
        try:
            processSurf(img,imageId,c,conn)
        except Exception,e:
            print "unable to process image "+imageId
            print str(e)
        numimg = numimg +1
        
        
        
def find(c):
    
        cmd = 'SELECT imageId from images WHERE imageId = N00369'
        #cmd = 'SELECT imageId from images WHERE imageId={iId}'.format(iId='N00369',)
        print cmd
        store = c.execute(cmd)
        print store 
    
def reteriveSurfRow(imageId,c):
    cmd = 'SELECT * FROM {tn} WHERE imageId = ?'.format(tn=table_name)
   
    c.execute(cmd,(imageId,))
    #c.execute("SELECT * from {tn}".format(tn=table_name))
    result = c.fetchone()
    return result

def reteriveSurfVals(imageId,c):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'SELECT * FROM {tn} WHERE imageId = ?'.format(tn=table_name)
   
    c.execute(cmd,(imageId,))
    #c.execute("SELECT * from {tn}".format(tn=table_name))
    result = c.fetchone()
    kpDes = pickle.loads(str(result[2]))
    #print kpDes
    keypoints, descriptors = surf.unblend_keypoints(kpDes)
    return keypoints, descriptors

#awsDW = dirm.outputDirectory + 'TurnerDbAWS1.sqlite'
#conn = sqlite3.connect(awsDW)

def main():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    
    dropDatabaseTable(c)
    createDatabaseTable(c)
    processSurfAllImages(c,conn)
    
    
    conn.commit()
    conn.close()

conn = sqlite3.connect(dirm.sqlite_file)
c = conn.cursor()

#dropDatabaseTable()
#createDatabaseTable()
#processSurfAllImages()


#img = cv2.imread('F:/2.jpg')
#processSurfAllImages()
#filename = 'dog'
#c.execute('PRAGMA foreign_keys = ON;')

#keypoints, descriptors  = reteriveSurfVals("A00909")
#c.execute("SELECT imageId from {tn}".format(tn=table_name))
#result = c.fetchall()
#print result
#print reteriveSurfRow("N03550")


conn.commit()
conn.close()
    