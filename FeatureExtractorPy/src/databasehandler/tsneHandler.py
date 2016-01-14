'''
Created on 14 Aug 2015

@author: Coryn
'''
import cPickle as pickle
import sqlite3
from util import dirm
import numpy as np
from databasehandler import imagesHandler
from util import util

table_name = "tsne"

def create_database_table():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'CREATE TABLE {tn} (name TEXT,store BLOB)'.format(tn=table_name)
    print cmd
    try:
        c.execute(cmd)
    except Exception,e:
        print e
            
    conn.commit()   
    conn.close()      
        
       
def drop_database_table():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'DROP TABLE IF EXISTS {tn}'.format(tn=table_name)
    print cmd
    c.execute(cmd)
    conn.commit()   
    conn.close()  
    
def storeTsneValsWIds(name,tsneVals,ids):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'DELETE FROM {tn} WHERE name=?'.format(tn=table_name)
    c.execute(cmd,(name,))
    conn.commit()
    combined = []
    combined.append(tsneVals.tolist())
    combined.append(ids)
    comb_pickle = pickle.dumps(combined, pickle.HIGHEST_PROTOCOL)
    comb_bin = sqlite3.Binary(comb_pickle)
    cmd = 'INSERT INTO {tn} (name, store) VALUES("{cn}", ?)'.format(tn=table_name,cn=name+'_tsne')
    c.execute(cmd,(comb_bin,))
    conn.commit()
    conn.close()
    
def getTSNEwithIds(name):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'SELECT store FROM {tn} WHERE name=?'.format(tn=table_name)
    c.execute(cmd,(name+'_tsne',))
    comb_pickle = c.fetchone()
    if comb_pickle != None:
        comb_pickle = comb_pickle[0]
        comb = pickle.loads(str(comb_pickle))
        tsneVals = comb[0]
        ids = comb[1]
    else:
        print "Tsne " + name + " Not found"
        return None
    
    conn.commit()
    conn.close()
    return tsneVals,ids

def storeTsne(name,tsneVals):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'DELETE FROM {tn} WHERE name=?'.format(tn=table_name)
    c.execute(cmd,(name,))
    conn.commit()
    tsne_pickle = pickle.dumps(tsneVals, pickle.HIGHEST_PROTOCOL)
    tsne_bin = sqlite3.Binary(tsne_pickle)
    cmd = 'INSERT INTO {tn} (name, store) VALUES("{cn}", ?)'.format(tn=table_name,cn=name+'_tsne')
    c.execute(cmd,(tsne_bin,))
    conn.commit()
    conn.close()
    
def getTSNE(name):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'SELECT store FROM {tn} WHERE name=?'.format(tn=table_name)
    c.execute(cmd,(name+'_tsne',))
    tsne_pickle = c.fetchone()
    if tsne_pickle != None:
        tsne_pickle = tsne_pickle[0]
        tsne_vals = pickle.loads(str(tsne_pickle))
        tsneVals = tsne_vals[0]
        ids = tsne_vals[1]
    else:
        print "Tsne " + name + " Not found"
        return None
    
    conn.commit()
    conn.close()
    return tsneVals


    
def storeLoc(name,loc):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'DELETE FROM {tn} WHERE name=?'.format(tn=table_name)
    c.execute(cmd,(name+"loc",))
    conn.commit()
    loc_pickle = pickle.dumps(loc, pickle.HIGHEST_PROTOCOL)
    loc_bin = sqlite3.Binary(loc_pickle)
    cmd = 'INSERT INTO {tn} (name, store) VALUES("{cn}", ?)'.format(tn=table_name,cn=name+"loc")
    c.execute(cmd,(loc_bin,))
    conn.commit()
    conn.close()
    
    
def getLoc(name):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'SELECT store FROM {tn} WHERE name=?'.format(tn=table_name)
    c.execute(cmd,(name+"loc",))
    loc_pickle = c.fetchone()
    if loc_pickle != None:
        loc_pickle = loc_pickle[0]
        loc = pickle.loads(str(loc_pickle))
    else:
        print "Locations " + name + " Not found"
        return None
    
    conn.commit()
    conn.close()
    return loc

def exportTsneWithFile(name):
    tsne_vals,ids = getTSNEwithIds(name)
    tsne_x,tsne_y = zip(*tsne_vals)
    tsne_x = np.array(tsne_x) * 50
    tsne_y = np.array(tsne_y) * 50
    urls = []
    filenames = []
    for id in ids:
        fullurl = imagesHandler.get_full_url(id)
        filename = fullurl.split(dirm.rootDirectory)[1]
        urls.append(imagesHandler.get_full_url(id))
        filenames.append(str(filename))
    results = zip(ids,tsne_x,tsne_y,filenames,urls)
    util.writetoCSV(results, name + "tsne with url")
    

create_database_table()
