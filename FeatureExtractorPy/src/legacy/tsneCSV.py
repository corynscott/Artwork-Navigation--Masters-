'''
Created on 16 Jul 2015

@author: Coryn
'''

import numpy as np
from util import dirm
from sklearn.manifold.t_sne import TSNE
from sklearn.decomposition.pca import PCA
from sklearn.preprocessing.data import Normalizer

from util import dirm
import csv


filename = dirm.outputDirectory + 'surfsubresized400extended30distrwh.csv'
file = open(filename)

data = np.loadtxt(file, delimiter = ',')
#X = data[:, 1:]
X = data
XAvr = []

for i in range(0, len(X)):
    sumofArray = sum(X[i])
    tempXi = X[i]/sumofArray
    XAvr.append(tempXi)
        
#normaliser = Normalizer().fit(X)
#X_norm = normaliser.transform(X)

#XAvrN = Normalizer().fit(XAvr).transform(XAvr)

#pca = PCA(n_components=50)
#pca.fit(X_norm)
#X_pca = pca.transform(X_norm)

#print X_pca


model = TSNE(n_components=2, random_state=0)
X_Tsne = model.fit_transform(XAvr)
#print len(X_Tsne)
#print len(X_Tsne[1])
#print X_Tsne
writetoCSV(X_Tsne,"surfsubresized400extended30tsneAvr")