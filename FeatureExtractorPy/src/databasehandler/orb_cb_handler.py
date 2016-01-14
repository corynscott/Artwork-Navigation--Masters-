'''
Created on 14 Aug 2015

@author: Coryn
'''
import cPickle as pickle
import sqlite3
from util import dirm

table_name = "orbCodebookDescriptors"

def create_database_table():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'CREATE TABLE {tn} (name TEXT,store BLOB)'.format(tn=table_name)
    print cmd
    c.execute(cmd)

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
    
def store_descriptors(desc):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    c.execute('DELETE FROM {tn} WHERE name="desc"'.format(tn=table_name))
    conn.commit()
    desc_pickle = pickle.dumps(desc, pickle.HIGHEST_PROTOCOL)
    desc_bin = sqlite3.Binary(desc_pickle)
    cmd = 'INSERT INTO {tn} (name, store) VALUES("{cn}", ?)'.format(tn=table_name,cn="desc")
    c.execute(cmd,(desc_bin,))
    conn.commit()
    conn.close()

def store_distributions(dist):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    c.execute('DELETE FROM {tn} WHERE name="dist"'.format(tn=table_name))
    conn.commit()
    dist_pickle = pickle.dumps(dist, pickle.HIGHEST_PROTOCOL)
    dist_bin = sqlite3.Binary(dist_pickle)
    cmd = 'INSERT INTO {tn}(name, store) VALUES("{cn}", ?)'.format(tn=table_name,cn="dist")
    c.execute(cmd,(dist_bin,))
    conn.commit()
    conn.close()
    
def store_estimator(est):
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    c.execute('DELETE FROM {tn} WHERE name="est"'.format(tn=table_name))
    conn.commit()
    est_pickle = pickle.dumps(est, pickle.HIGHEST_PROTOCOL)
    est_bin = sqlite3.Binary(est_pickle)
    cmd = 'INSERT INTO {tn}(name, store) VALUES("{cn}", ?)'.format(tn=table_name,cn="est")
    c.execute(cmd,(est_bin,))
    conn.commit()
    conn.close()
    
def get_descriptors():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'SELECT store FROM {tn} WHERE name="desc"'.format(tn=table_name)
    c.execute(cmd)
    desc_pickle = c.fetchone()
    if desc_pickle != None:
        desc_pickle = desc_pickle[0]
        desc = pickle.loads(str(desc_pickle))
    else:
        print "No Descriptor found"
        return None
    
    conn.commit()
    conn.close()
    return desc

def get_distributions():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'SELECT store FROM {tn} WHERE name="dist"'.format(tn=table_name)
    c.execute(cmd)
    dist_pickle = c.fetchone()
    if dist_pickle != None:
        dist_pickle= dist_pickle[0]
        dist = pickle.loads(str(dist_pickle))
    else:
        print "No Distribution found"
        return None
    
    conn.commit()
    conn.close()
    return dist

def get_estimator():
    conn = sqlite3.connect(dirm.sqlite_file)
    c = conn.cursor()
    cmd = 'SELECT store FROM {tn} WHERE name="est"'.format(tn=table_name)
    c.execute(cmd)
    est_pickle = c.fetchone()
    if est_pickle != None:
        est_pickle= est_pickle[0]
        est = pickle.loads(str(est_pickle))
    else:
        print "No Estimator found"
        return None
    
    conn.commit()
    conn.close()
    return est
