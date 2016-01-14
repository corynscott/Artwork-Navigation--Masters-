'''
Created on 5 Jul 2015

@author: Coryn
'''
import sqlite3
from util import dirm
import os
from features import hog

table_name = "hog"

numColumns = hog.bin_n*4
columnsWT= ''
columns = ''
# method used to generate the SQL commands for the bins as part of the declaration 
def generate_columns_with_type():
    columnsWT= ''
    for x in range (0,numColumns):
        columnsWT = columnsWT + 'Bin_' + str(x) + ' INTEGER, '
    columnsWT =  columnsWT[:-2]
    return columnsWT

# method used to generate the SQL commands for the bins as part of the declaration 
def generate_columns():
    columns= ''
    for x in range (0,numColumns):
        columns = columns + 'Bin_' + str(x) + ', '
    columns =  columns[:-2]
    return columns

# Creates the Database Table
def create_database_table():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    
    cmd = 'CREATE TABLE {tn} (imageId TEXT PRIMARY KEY, {bins}, FOREIGN KEY(imageId) REFERENCES images(imageId))'.format(tn=table_name,bins=generate_columns_with_type())
    print cmd
    c.execute(cmd)

    conn.commit()
    conn.close()

#drops the database table         
def drop_database_table():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    
    cmd = 'DROP TABLE IF EXISTS {tn}'.format(tn=table_name)
    print cmd
    c.execute(cmd)

    conn.commit()
    conn.close()

# go through all images in the database and process the HOG for each
def process_hog():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    
    print 'Adding Hog Values for all images stored in the SQL Database.'
    c.execute('SELECT * FROM images')
    images =c.fetchall()
    numimg = 0
    for image in images:
        if numimg%100==0:
                print numimg
        try:
            imageId = image[0]
            imageURL = image[1]
            hogVals = str(hog.extract_hog_histogram(imageURL).tolist())
            hogVals = hogVals.replace('[', '').replace(']', '')
            if len(hogVals)>5:
                cmd = 'INSERT INTO {tn}(imageId,{bins}) VALUES((SELECT imageId from images WHERE imageId="{iId}"), {hv} )'.format(tn=table_name,bins=generate_columns(),iId=imageId,hv=hogVals)
                
                try:
                    c.execute(cmd)
                    conn.commit()
                    numimg = numimg +1
                except sqlite3.IntegrityError:
                    print('ERROR: ID already exists in PRIMARY KEY column {}'.format(imageId))
            else:
                print 'Error Processing '+ imageId                   
        #print cmd
        except Exception,e:
            print str(e)
            print 'Error Procesing:' + imageURL
            
        
    conn.commit()
    conn.close()
    
# get the HOG stored in the database for all the images        
def getHogValsforAllImages():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'SELECT * FROM {tn}'.format(tn=table_name)
    c.execute(cmd)
    results = c.fetchall()
    conn.close()
    return results

def main():
    drop_database_table()
    create_database_table()
    process_hog()
    


    