'''
Created on 12 Jul 2015

@author: Coryn
'''
import sqlite3
from util import dirm
import csv

#used to access locally
aws_sqlite = dirm.outputDirectory + dirm.awsOutputDatabaseName  + '.sqlite'
local_sqlite = dirm.sqlite_file

conn = sqlite3.connect(local_sqlite)
c = conn.cursor()


c.execute('SELECT * FROM hog')
#images =c.fetchall()

with open(dirm.outputDirectory +"hog.csv", "wb") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in c.description]) # write headers
    csv_writer.writerows(c)


conn.close()

