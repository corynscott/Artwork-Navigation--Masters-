'''
Created on 23 Aug 2015
This module provides various imagemanagement tools
@author: Coryn
'''
from databasehandler import imagesHandler
import cv2
from util import dirm
import sqlite3

def resize_image(img,ratio,method):
    img_resized = cv2.resize(img, None, None, ratio, ratio, method);
    return img_resized

def crop_image(img,crop_amount):
    height = img.shape[0]
    width = img.shape[1]
    x = crop_amount
    y = crop_amount
    crop_img = img[y:height-y,x:width-x]
    return crop_img
    
# function resizes all of the images in the current database and stores in meta sub-folder called small
def resize_all_images(size):
    imageids = imagesHandler.get_all_img_ids_string()
    for img_id in imageids:
        img = imagesHandler.get_image(img_id)
        url = imagesHandler.get_full_url(img_id)
        filename = url.split(dirm.rootDirectory)[1]
        imgr = cv2.resize(img, (size, size))
        cv2.imwrite(dirm.rootDirectory+"/small/"+ filename, imgr )
        
def load_image_from_file(filename):
    return cv2.imread(dirm.outputDirectory+filename+".jpg")
    
def export_urls_of_images_as_txt():
    
    imagesHandler.main()
    
    local_sqlite = dirm.sqlite_file
    
    conn = sqlite3.connect(local_sqlite)
    
    c = conn.cursor()
    
    c.execute('SELECT fullURL FROM images')
    results = c.fetchall()
    print len(results)
    file = open(dirm.outputDirectory+"localurl.txt", "w")
    for row in results:
        out = str(row[0])
        file.write("%s\n" % out)
    
    file.close()
    
    conn.close()