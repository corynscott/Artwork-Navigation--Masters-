'''
Created on 5 Jul 2015
@author: Coryn
'''
import sqlite3
from util import dirm
import os
from features import colour

RGB_table_name = "colour_distribution_RGB"

LAB_table_name = "colour_distribution_LAB"

numColumns = colour.num_bins

# method used to generate the SQL commands for the bins as part of the declaration 
def generate_columns_with_type():
    columnsWT= ''
    for x in range (0,(numColumns-2)):
        columnsWT = columnsWT + 'Bin_' + str(x) + ' INTEGER, '
    columnsWT =  columnsWT[:-2]
    
    return columnsWT

# method used to generate the SQL commands for the bins as part of the declaration 
def generate_columns():
    columns= ''
    for x in range (0,numColumns-2):
        columns = columns + 'Bin_' + str(x) + ', '
    columns =  columns[:-2]
    return columns

# Creates the Database Table
def create_database_table(table_name):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'CREATE TABLE {tn} (imageId TEXT PRIMARY KEY, {bins}, FOREIGN KEY(imageId) REFERENCES images(imageId))'.format(tn=table_name,bins=generate_columns_with_type())
    print cmd
    c.execute(cmd)
    conn.commit()
    conn.close()
    
#drops the database table       
def drop_database_table(table_name):
    
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'DROP TABLE IF EXISTS {tn}'.format(tn=table_name)
    print cmd
    c.execute(cmd)
    conn.commit()
    conn.close()
    
# go through all images in the database and process the colour distribution for each
def process_colour_dist_for_all_images(table_name):       
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    print 'Adding colour Distribution for all images stored in the SQL Database.'
    c.execute('SELECT * FROM images')
    images =c.fetchall()
    numimg = 0
    for image in images:
        if numimg%100==0:
                print numimg
        imageId = image[0]
        imageURL = image[1]
        if table_name == RGB_table_name:
            dist = colour.extract_colour_hist_rgb(imageURL)
        elif table_name == LAB_table_name:
            dist = colour.extract_colour_dist_lab(imageURL)
        distList = dist.replace('[', '').replace(']', '')
        distList.strip()    # Remove whitespace
        if len(distList)>5:
            cmd = 'INSERT INTO {tn}(imageId,{bins}) VALUES((SELECT imageId from images WHERE imageId="{iId}"), {dl} )'.format(tn=table_name,bins=generate_columns(),iId=imageId,dl=distList)
            numimg = numimg +1
            try:
                c.execute(cmd)
                conn.commit()
            except sqlite3.IntegrityError:
                print('ERROR: ID already exists in PRIMARY KEY column {}'.format(imageId))
        else:
            print 'Error Processing '+ imageId
    conn.commit()
    conn.close()
    
# get the colourDistributions stored in the databse for all the images
def getColourDistForAllImages(colour_space):
    if colour_space == "RGB":
        table_name = RGB_table_name
    elif colour_space == "LAB":
        table_name = LAB_table_name
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'SELECT * FROM {tn}'.format(tn=table_name)
    c.execute(cmd)
    results = c.fetchall()
    conn.close()
    return results
    

def main(colour_space):
    if colour_space == "RGB":
        table_name = RGB_table_name
    elif colour_space == "LAB":
        table_name = LAB_table_name
    drop_database_table(table_name)
    create_database_table(table_name)
    process_colour_dist_for_all_images(table_name)
    

