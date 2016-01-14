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

table_name = "surf"

numColumns = 128

def generateColumnsWithType():
    columnsWT= ''
    for x in range (0,(numColumns)):
        columnsWT = columnsWT + 'Bin_' + str(x) + ' INTEGER, '
    columnsWT =  columnsWT[:-2]
    
    return columnsWT

def generateColumns():
    columns= ''
    for x in range (0,numColumns):
        columns = columns + 'Bin_' + str(x) + ', '
    columns =  columns[:-2]
    return columns


columnsWT = generateColumnsWithType()
columns = generateColumns()


def createDatabaseTable():
    cmd = 'CREATE TABLE {tn} (imageId TEXT, x INTEGER, y INTEGER, size INTEGER, angle INTEGER, response INTEGER, octave INTEGER, class_id INTEGER, {desc}, FOREIGN KEY(imageId) REFERENCES images(imageId))'.format(tn=table_name,desc=columnsWT)
    print cmd
    c.execute(cmd)

       
def dropDatabaseTable():
    cmd = 'DROP TABLE IF EXISTS {tn}'.format(tn=table_name)
    print cmd
    c.execute(cmd)

def processSurf(img,imageId):
    
    kp,des = surf.calc_surf(img)
    i=0
    for point in kp:
        x=point.pt[0]
        y=point.pt[1]
        size=point.size
        angle=point.angle
        response=point.response
        octave=point.octave
        class_id=point.class_id
        descriptor = des[1]
        
        i=i+1
        
        desList = str(descriptor.tolist())
        desList= desList.replace('[', '').replace(']', '')
        desList.strip()    
    
        if len(desList)>5:
            #print distList
            cmd = 'INSERT INTO {tn}(imageId, x, y , size , angle , response , octave , class_id, {desc}) VALUES((SELECT imageId from images WHERE imageId="{iId}"), {xi}, {yi}, {sizei}, {anglei}, {responsei}, {octavei}, {class_idi}, {dl} )'.format(tn=table_name,desc=columns,iId=imageId,xi=x, yi=y, sizei=size, anglei=angle, responsei=response, octavei=octave, class_idi=class_id, dl=desList)
            
            try:
                c.execute(cmd)
                conn.commit()
            except sqlite3.IntegrityError:
                print('ERROR: ID already exists in PRIMARY KEY column {}'.format(imageId))
                            
            #print cmd
        else:
            print 'Error Processing '+ imageId
                
        
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
processSurfAllImages()
#img = cv2.imread('F:/2.jpg')
#processSurf(img, 'N00369')
#filename = 'dog'
#c.execute('PRAGMA foreign_keys = ON;')

conn.commit()
conn.close()
    