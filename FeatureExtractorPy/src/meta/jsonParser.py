'''
Created on 27 Aug 2015

@author: Coryn
'''
import json
from pprint import pprint


def find_values(url):
   
    ids = []
    names = []

    def _decode_dict(a_dict):
        try: 
            ids.append(a_dict['id'])
            names.append(a_dict['name'])
            
        except KeyError: pass
        return a_dict

    datafile = open(url)
    #data = 
    try:
        json_data = json.load(datafile)
        subjects = json_data['subjects']
        subjects_json = json.dumps(subjects)
        json.loads(subjects_json, object_hook=_decode_dict)
    except:
        print "no metadata avaliabel for:", url
    return ids,names

#print find_values("f:/d40068-63836.json")
