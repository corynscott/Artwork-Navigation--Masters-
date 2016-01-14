'''
Created on 14 Aug 2015

@author: Coryn
'''
def calc_Grey_hist(im):
   
    if len(im.shape)!=2:
        im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    hist_item = cv2.calcHist([im],[0],None,[numBins],[0,numBins])
    cv2.normalize(hist_item,hist_item,0,numBins,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    return hist


def buildCodebookFromDatabase():
   
    awsDW = dirm.outputDirectory + 'TurnerDbAWSSub1.sqlite'
    #conn = sqlite3.connect(awsDW)
    localAWS = dirm.outputDirectory + dirm.awsOutputDatabaseName + "1.sqlite"
    print localAWS
    conn = sqlite3.connect(localAWS)
    c = conn.cursor()
    
    c.execute('SELECT * FROM surfAll400')
    images =c.fetchall()
    #images = images[:10]
    #print images
    numimg = 0
    allDescriptors = []
    for image in images:   #print image
        imageId = image[0]
        numKeypoints = image[1]
        kpDes = pickle.loads(str(image[2]))
        keypoints, descriptors = surf.unblend_keypoints(kpDes)
        allDescriptors.append(descriptors)

        numimg = numimg +1
        
    #print allDescriptors[0][0] 
    
    concatDesc = []
    for image in allDescriptors:
        for desc in image:
            concatDesc.append(desc)
        
    
    print len(concatDesc)
    print len(concatDesc[0])
    return concatDesc