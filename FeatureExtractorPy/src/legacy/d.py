'''
Created on 29 Aug 2015

@author: Coryn
'''
from databasehandler import colourHandler
import numpy as np
a = [[2,3,2],[3,4,3]]
c = np.delete(a,0,1)
print c
colour_data = colourHandler.getColourDistForAllImages("RGB")
colour_data = np.array(colour_data,dtype=None)
colour_data= np.delete(colour_data,0,1)
print colour_data