from databasehandler import imagesHandler
import os
from meta import jsonParser
from zmq.utils.constant_names import all_names


def getjsonfile(image_id):
    image_id = str(image_id).lower()
    matadataloation = "f:/metadata/"
    char = image_id[0]
    num = image_id[1:4]
    folder = "f:/metadata/"+char+"/"+num+"/"
    for i in os.listdir(folder):
       # print i,image_id
        if i.startswith(image_id):
            return folder+i
    
    print "error",folder
    return None
    
def collectallmeta():
    image_ids = imagesHandler.get_all_img_ids_string()
    all_names = []
    all_ids = []
    names_turp = []
    ids_turp = []
    for id in image_ids:
        json_url = getjsonfile(id)
        
        ids,names = jsonParser.find_values(json_url)
        all_names.extend(names)
        all_ids.extend(ids)
        names_turp.append(names)
        ids_turp.append(ids)
    
    return set(all_ids),set(all_names), ids_turp,names_turp
   
    
# all_ids,all_names,ids_turp,names_turp= collectallmeta()
# print all_ids
# print len(all_ids)
# print all_names
# print len(all_names)
#     