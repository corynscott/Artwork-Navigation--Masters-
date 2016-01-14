'''
Created on 4 Aug 2015

@author: Coryn
'''
from databasehandler import imagesHandler, colourHandler, hogHandler, tsneHandler
from databasehandler import surf_cb_handler,tsneHandler
from mapping import plot_visualisation, tsne
import varKmeans
from features import interest_point_detectors, colour
import numpy as np
import math
import cv2
from codebook_bow import surf_codebook, sift_codebook, orb_codebook
from util import dirm, image_managment
import timeit

##!!! SET THE SUB Sample!!!!#



#tsne Params
n_clusters = 30


#surf params
hessian_threshold = 400
resize_ratio = 0.3
resize_method = cv2.INTER_CUBIC
crop_amount = 0
def run():
    #EXTRACT ALL OUR FEATURES AND STORE THEM IN THE SQL DATABASE
    imagesHandler.main()
    colourHandler.main("RGB")
    colourHandler.main("LAB")
    hogHandler.main()
    
    surf_start = timeit.default_timer()
    surf_codebook.run_codebook(n_clusters,hessian_threshold, resize_ratio, resize_method, crop_amount)
    surfRunTime = timeit.default_timer() - surf_start
    
    sift_start = timeit.default_timer()
    sift_codebook.run_codebook(n_clusters, resize_ratio, resize_method, crop_amount)
    siftRunTime = timeit.default_timer() - sift_start
    
    orb_start = timeit.default_timer()
    orb_codebook.run_codebook(n_clusters, resize_ratio, resize_method, crop_amount)
    orbRunTime = timeit.default_timer() - orb_start
    print "SurfRunttime:",surfRunTime,"siftRuntime:",siftRunTime,"orbRt",orbRunTime
    
    # PERFORM TSNE
    tsneHandler.drop_database_table()
    tsneHandler.create_database_table()
    
    RGB_col_tsne,R_c_ids = tsne.TSNE_General(colourHandler.RGB_table_name)
    LAB_col_tsne,L_c_ids = tsne.TSNE_General(colourHandler.LAB_table_name)
    
    hog_tsne, h_ids = tsne.TSNE_General(hogHandler.table_name)
    
    gist_tsne,g_ids = tsne.TSNE_Gist("gist_tsne", "gistvals")
    
    surf_tsne, su_ids = tsne.TSNE_Surf("surf_ht"+str(hessian_threshold)+"_rz"+str(resize_ratio)+"_cr"+str(crop_amount) +"_n"+str(n_clusters))
    orb_tsne, o_ids = tsne.TSNE_orb("orb_rz"+str(resize_ratio)+"_cr"+str(crop_amount) +"_n"+str(n_clusters))
    sift_tsne, si_ids = tsne.TSNE_sift("sift_rz"+str(resize_ratio)+"_cr"+str(crop_amount) +"_n"+str(n_clusters))
    
    # get from sql
    #col_tsne, c_ids = tsneHandler.getTSNEwithIds(colourHandler.table_name)
    #hog_tsne, h_ids = tsneHandler.getTSNEwithIds(hogHandler.table_name)
    #surf_tsne, s_ids = tsneHandler.getTSNEwithIds("surf_n"+str(n_clusters))
    
    #Plot    
    plot_visualisation.plot_raw_TSNE(RGB_col_tsne,R_c_ids,colourHandler.RGB_table_name)
    plot_visualisation.plot_raw_TSNE(LAB_col_tsne, L_c_ids, colourHandler.LAB_table_name)
    plot_visualisation.plot_raw_TSNE(hog_tsne,h_ids,hogHandler.table_name)
    plot_visualisation.plot_raw_TSNE(gist_tsne, g_ids, "gist")
    
    plot_visualisation.plot_raw_TSNE(surf_tsne,su_ids,"surf_ht"+str(hessian_threshold)+"_rz"+str(resize_ratio)+"_cr"+str(crop_amount) +"_n"+str(n_clusters) + '_tsne')
    plot_visualisation.plot_raw_TSNE(orb_tsne,o_ids,"orb_rz"+str(resize_ratio)+"_cr"+str(crop_amount) +"_n"+str(n_clusters) + '_tsne')
    plot_visualisation.plot_raw_TSNE(sift_tsne,si_ids,"sift_rz"+str(resize_ratio)+"_cr"+str(crop_amount) +"_n"+str(n_clusters) + '_tsne')
    
    #Export tsne results to csv to be processed by gephi ect
    tsneHandler.exportTsneWithFile(colourHandler.RGB_table_name)
    tsneHandler.exportTsneWithFile(colourHandler.LAB_table_name)
    tsneHandler.exportTsneWithFile(hogHandler.table_name)
    tsneHandler.exportTsneWithFile("gist_tsne")
    tsneHandler.exportTsneWithFile("surf_ht"+str(hessian_threshold)+"_rz"+str(resize_ratio)+"_cr"+str(crop_amount) +"_n"+str(n_clusters))
    tsneHandler.exportTsneWithFile("orb_rz"+str(resize_ratio)+"_cr"+str(crop_amount) +"_n"+str(n_clusters))
    tsneHandler.exportTsneWithFile("sift_rz"+str(resize_ratio)+"_cr"+str(crop_amount) +"_n"+str(n_clusters))
    

def run_interactive_ux(filename):
    #PLOT
    #col_tsne, c_ids = tsneHandler.getTSNEwithIds(colourHandler.table_name)
    #hog_tsne, h_ids = tsneHandler.getTSNEwithIds(hogHandler.table_name)
    #surf_tsne, s_ids = tsneHandler.getTSNEwithIds("surf_n"+str(n_clusters))
    #plot_visualisation.plot_raw_TSNE(surf_tsne,s_ids,"surf_rz_ht_"+ str(hessian_threshold) +"_n"+str(n_clusters) + '_tsne')
    print "loading image"
    img = image_managment.load_image_from_file(filename)
    plot_visualisation.displayInteractiveImage(img, filename)


#run()


# name = "surf_rz_ht_200_n30_tsne_raw"
# run_interactive_ux(name)
# plot_visualisation.lookup_image_by_id("D24872", name)
#colourHandler.main(colour_space)
#col_tsne,c_ids  = tsne.TSNE_General(colourHandler.table_name)
#plot_visualisation.plot_raw_TSNE(col_tsne,c_ids,colourHandler.RGB_table_name)
#hogHandler.main()
#hog_tsne, h_ids = tsne.TSNE_General(hogHandler.table_name)