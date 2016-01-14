'''
Created on 2 Jul 2015

@author: Coryn
'''
import sqlite3
from util import dirm
import os
import cv2

table_name = "images"
id_column = 'imageId'
field_type = 'TEXT'

# Creates the Database Table
def create_database_table():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    
    cmd = 'CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY, url TEXT, fullURL TEXT)'
    c.execute(cmd\
        .format(tn=table_name, nf=id_column, ft=field_type))
    print cmd
    
    conn.commit()   
    conn.close()      
        
#drops the database table      
def drop_database_table():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    
    c.execute('DROP TABLE IF EXISTS images ')
    
    conn.commit()   
    conn.close()

# go through the director set in the dirm module and adds eacth image to the database
def add_all_images_to_db():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    numimg = 0
    print 'Adding images from ' + dirm.rootDirectory + " to SQL Database."
    print 'Images:' + dirm.rootDirectory
    for root, dirs, files in os.walk(dirm.rootDirectory):
        for file in files:
            if numimg%100==0:
                print numimg
            if file.endswith(".jpg"):
                filename = str(file).partition("_")[0]
                filename = str(filename)
                fullurl = str(os.path.join(root, file))
                imgURL = fullurl.replace(dirm.rootDirectory, "/")
                try:
                    c.execute('INSERT INTO images(imageId,url,fullURL) VALUES(?,?,?)', (filename,imgURL,fullurl,))
                    
                    numimg = numimg +1
                except sqlite3.IntegrityError:
                    print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))
    conn.commit()   
    conn.close()      
              
#returns all the rows in the image database
def get_all_img_rows():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'SELECT * from images'
    c.execute(cmd)
    allImg = c.fetchall()
    conn.close()
    return allImg    

#returns all the ids of the images stored in the database
def get_all_img_ids():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    
    cmd = 'SELECT imageId from images'
    c.execute(cmd)
    allImgIds = c.fetchall()
    
    conn.close()
    return allImgIds

#return all the ids of the images stored in the database as strings
def get_all_img_ids_string():
    idsT = get_all_img_ids()
    ids = []
    for id in idsT:
        ids.append(str(id[0]))
    return ids

# returns a specific image based on the image id
def get_image(imageid):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    
    cmd = 'SELECT url from images WHERE imageId=?'
    c.execute(cmd,(imageid,))
    imageURL = c.fetchone()[0]
    #print imageURL
    
    img = cv2.imread(dirm.rootDirectory + imageURL)
    
    conn.close()
    return img

# get the full url of an image based on its imageid
def get_full_url(imageid):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    
    cmd = 'SELECT fullURL from images WHERE imageId=?'
    c.execute(cmd,(imageid,))
    imageURL = c.fetchone()[0]
    conn.close()
    return str(imageURL)

def main():
    drop_database_table()
    create_database_table()
    add_all_images_to_db()
    