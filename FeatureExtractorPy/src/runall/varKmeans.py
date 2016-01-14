'''
Created on 18 Aug 2015

@author: Coryn
'''
'''
Created on 4 Aug 2015

@author: Coryn
'''
from databasehandler import imagesHandler, colourHandler, hogHandler,\
    tsneHandler
from util import dirm
from codebook_bow import surf_codebook
from mapping import tsne
from mapping import plot_visualisation


##!!! SET THE SUB Sample!!!!#



def perfromTsneOnNCl(n_clusters):
    surf_codebook.main(n_clusters)
    
    #PERFORM TSNE
    surf_tsne, s_ids = tsne.TSNE_Surf("surf_n"+str(n_clusters))
    
    #PLOT
    #surf_tsne, s_ids = tsneHandler.getTSNEwithIds("surf_n"+str(n_clusters))
    plot_visualisation.plot_raw_TSNE(surf_tsne,s_ids,"surf"+str(n_clusters)+'_tsne')
    
def varKMeansAccRang():
    n_cluster_range = [2,3,5,10,15]
    for n_clusters in n_cluster_range:
        perfromTsneOnNCl(n_clusters)
        
#varKMeansAccRang()