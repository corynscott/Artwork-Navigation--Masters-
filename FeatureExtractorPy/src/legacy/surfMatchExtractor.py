'''
Created on 6 Aug 2015

@author: Coryn
'''
import sqlite3
from util import dirm
from mapping import displaySurfArray
from databasehandler import imagesHandler

aws_sqlite = dirm.outputDirectory + dirm.awsOutputDatabaseName  + '1.sqlite'
local_sqlite = dirm.sqlite_file

#hardCodedArray = [[22,14,12,15,23],[18,6,4,7,19],[11,3,1,2,10],[20,8,5,9,21], [24,16,13,17,25]]
hardCodedArray = [[21,13,11,14,22],[17,5,3,6,18],[10,2,0,1,9],[19,7,4,8,20], [23,15,12,16,24]]
emptyMean = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
emptyNum = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

def getMathes(imageId):

    conn = sqlite3.connect(aws_sqlite)
    c = conn.cursor()
    
    cmdNum = "SELECT imageId1, imageId2, numMatches, meanDistance, numMatches, meanDistance FROM surfMatches400 WHERE imageId1 = ? AND imageId2 <> ? ORDER BY numMatches DESC"
    cmdMean = "SELECT imageId1, imageId2, numMatches, meanDistance, numMatches, meanDistance FROM surfMatches400 WHERE imageId1 = ? AND imageId2 <> ? ORDER BY meanDistance DESC"
    
    c.execute(cmdNum,(imageId,imageId,))
    resultsSortedByNumMatches = c.fetchall()
    
    c.execute(cmdMean,(imageId,imageId,))
    resultsSortedByMean = c.fetchall()
    
    
    #print len(resultsSortedByMean)
    #print resultsSortedByMean
    print resultsSortedByNumMatches
    
    conn.close()
    return resultsSortedByNumMatches,resultsSortedByMean



def generateImageArrayMean(imageId):
    matchesNum,matchesMean = getMathes(imageId)
    
    imageArrayMean = emptyMean
    r = 0
    c = 0
    
    for row in hardCodedArray:
        c = 0
        for col in row:
            print col
            if col==0:
                centralImage = imagesHandler.getImage(imageId)
                imageArrayMean[r][c] = centralImage
                
            else:
                print 'pos:', r,c, 'is getting image ',  str(matchesMean[col-1][1]) 
                imgMean = imagesHandler.getImage(str(matchesMean[col-1][1]))
                imageArrayMean[r][c] = imgMean
            c = c +1
        r = r+1
        
    return imageArrayMean

def generateImageArrayNum(imageId):
    matchesNum,matchesMean = getMathes(imageId)
    
    matchesNum = matchesNum[:24]
    
    imageArrayNum = emptyNum
    r = 0
    c = 0
    
    for row in hardCodedArray:
        c = 0
        for col in row:
            if col==0:
                centralImage = imagesHandler.getImage(imageId)
                imageArrayNum[r][c] = centralImage
                
            else:
               # print 'pos:', r,c, 'id ',  col-1
              #  print 'pos:', r,c, 'is getting image ',  str(matchesNum[col-1][1])
                imgNum = imagesHandler.getImage(str(matchesNum[col-1][1]))
                imageArrayNum[r][c] = imgNum
            c = c +1
        r = r+1
        
    return imageArrayNum
    
imageId = "N00493"
imageArrayNum = generateImageArrayNum(imageId)
#imageArrayMean = generateImageArrayMean(imageId)
#print imageArrayMean

displaySurfArray.showImages(imageArrayNum)