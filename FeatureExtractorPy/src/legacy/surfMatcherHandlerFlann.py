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
import surfHandlerP


table_name = "surfMatchesFl" + str(surf.hassianThreshold)

def createDatabaseTable(c):
    cmd = 'CREATE TABLE {tn} (imageId1 TEXT, imageId2 TEXT, numMatches INTEGER, meanDistance REAL, numMatchesAT INTEGER, meanDistanceAT REAL, matches BLOB, matchesAT BLOB, FOREIGN KEY(imageId1) REFERENCES images(imageId),FOREIGN KEY(imageId2) REFERENCES images(imageId))'.format(tn=table_name)
    print cmd
    c.execute(cmd)

       
def dropDatabaseTable(c):
    cmd = 'DROP TABLE IF EXISTS {tn}'.format(tn=table_name)
    print cmd
    c.execute(cmd)
    
def store(imgId1,imgId2, matches, numMatches, meanDistance, matchesAT, numMatchesAT, meanDistanceAT,c,conn):

    matches_pickle = pickle.dumps(matches, pickle.HIGHEST_PROTOCOL)
    matches_bin = sqlite3.Binary(matches_pickle)
    
    matchesAT_pickle = pickle.dumps(matchesAT, pickle.HIGHEST_PROTOCOL)
    matchesAT_bin = sqlite3.Binary(matchesAT_pickle)
    #print numMatches, meanDistance, numMatchesAT, meanDistanceAT
    cmd = 'INSERT INTO {tn}(imageId1, imageId2, numMatches, meanDistance, numMatchesAT, meanDistanceAT, matches, matchesAT) VALUES((SELECT imageId from images WHERE imageId="{iId1}"),(SELECT imageId from images WHERE imageId="{iId2}"), {numMat}, {meanDis}, {numMatAT}, {meanDisAT}, ?, ?)'.format(tn=table_name,iId1=imgId1,iId2=imgId2,numMat=numMatches, meanDis=meanDistance, numMatAT=numMatchesAT, meanDisAT=meanDistanceAT)
    #print cmd   
    try:
        c.execute(cmd,(matches_bin,matchesAT_bin,))
        conn.commit()
    except sqlite3.IntegrityError:
        print('ERROR: ID already exists in PRIMARY KEY column {id1},{id2}'.format(id1=imgId1,id2=imgId1))
                    
                
        

def matchAllImagesFlann(c,conn):
   
    c.execute('SELECT * FROM images')
    images =c.fetchall()
    #print images
    numimg = 0
    for image1 in images:
        if numimg%50==0:
                print numimg
        imageId1 = image1[0]
        imageURL1 = image1[1]
        subNumImg = 0
        print imageId1
        for image2 in images:
            if subNumImg%50==0:
                print str(image1) +':' + str(subNumImg)
            
            imageId2 = image2[0]
            imageURL2 = image1[1]
       
            #print dirm.rootDirectory + imageURL
            try:
                
                kp1, des1 = surfHandlerP.reteriveSurfVals(imageId1,c)
                kp2, des2 = surfHandlerP.reteriveSurfVals(imageId2,c)
                
                matches,numMatches, meanDistance, matchesAT,numMatchesAT, meanDistanceAT  = surf.flannMatcher(kp1, des1, kp2, des2)
                
                store(imageId1, imageId2, matches, numMatches, meanDistance, matchesAT,numMatchesAT, meanDistanceAT,c,conn)
            except Exception, e:
                print "unable to process image "+imageId1 + ", " + imageId2
                print str(e)
            subNumImg = subNumImg + 1
        numimg = numimg +1
        
               
               
def bowKn(c,con):
    
    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    
    flann = cv2.FlannBasedMatcher(index_params,search_params)
   
    c.execute('SELECT * FROM images')
    images =c.fetchall()
    images = images[:5]
    #print images
    numimg = 0
    for image1 in images:
               
        
        if numimg%50==0:
                print 'processed so far:' + str(numimg)
        imageId1 = image1[0]
        imageURL1 = image1[1]
        
        kp1, des1 = surfHandlerP.reteriveSurfVals(imageId1,c)
        
    
        flann.add([des1])
        
        numimg = numimg + 1
    flann.train()
    print len(flann.getTrainDescriptors())
    imageId2 = images[3][0]
    kp2, des2 = surfHandlerP.reteriveSurfVals(imageId2,c)
    print len(des2)
            
    matches = flann.knnMatch(des2,k=2)
    
    print len(matches)
    print matches[16]
    match = matches[1650]
    print match.distance, match.trainIdx, match.queryIdx, match.imgIdx
    matchesA = [0,0,0,0,0,0,0]
    #for match in matches:
     #   print match.imgIdx
      #  #matchesA[match.imgIdx] = matchesA[match.imgIdx] + 1
    #print matchesA
    
def bow(c,con):
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    
    c.execute('SELECT * FROM images')
    images =c.fetchall()
    images = images[:5]
    #print images
    numimg = 0
    for image1 in images:
               
        
        if numimg%50==0:
                print 'processed so far:' + str(numimg)
        imageId1 = image1[0]
        imageURL1 = image1[1]
        
        kp1, des1 = surfHandlerP.reteriveSurfVals(imageId1,c)
        
    
        bf.add(des1)
        
        numimg = numimg + 1
        
        
    bf.train()
    print len(bf.getTrainDescriptors())
    imageId2 = images[3][0]
    kp2, des2 = surfHandlerP.reteriveSurfVals(imageId2,c)
    print len(des2)
            
    matches = bf.match(des2)
    
    print len(matches)
    print matches[16]
    match = matches[1650]
    print match.distance, match.trainIdx, match.queryIdx, match.imgIdx
    matchesA = [0,0,0,0,0,0,0]
    #for match in matches:
     #   print match.imgIdx
      #  #matchesA[match.imgIdx] = matchesA[match.imgIdx] + 1
    #print matchesA      

    
def reteriveMatchRow(imageId,c):
    cmd = 'SELECT * FROM {tn} WHERE imageId = ?'.format(tn=table_name)
   
    c.execute(cmd,(imageId,))
    #c.execute("SELECT * from {tn}".format(tn=table_name))
    result = c.fetchone()
    return result

def reteriveMatches(imageId,c):
    cmd = 'SELECT * FROM {tn} WHERE imageId = ?'.format(tn=table_name)
   
    c.execute(cmd,(imageId,))
    #c.execute("SELECT * from {tn}".format(tn=table_name))
    result = c.fetchone()
    matches = pickle.loads(str(result[4]))
    return matches

def main():
    #awsDW = dirm.outputDirectory + 'TurnerDbAWS1.sqlite'
    #conn = sqlite3.connect(awsDW)
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    
    
    dropDatabaseTable(c)
    createDatabaseTable(c)
    matchAllImagesFlann(c,conn)  
    
    
    
#main()

def main2():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    bow(c, conn)
    conn.commit()
    conn.close()
    
main2()
    
#awsDW = dirm.outputDirectory + 'TurnerDbAWS1.sqlite'
##conn = sqlite3.connect(awsDW)
#conn = sqlite3.connect(dirm.sqlite_file)
#c = conn.cursor()


    
    
#imgId1 = "N00539"
#imgId2 = "N00540"
#kp1, des1 = surfHandlerP.reteriveSurfVals(imgId1)
#kp2, des2 = surfHandlerP.reteriveSurfVals(imgId2)
#matches, numMatches, meanDistance = surf.bfMatch(kp1, des1, kp2, des2)




#conn.commit()
#conn.close()
    