'''
Created on 27 Aug 2015

@author: Coryn
'''
from meta import extractmeta
from sklearn.feature_extraction.text import CountVectorizer
from unidecode import unidecode
def metabagofwords():
    vectorizer = CountVectorizer(analyzer = "word",   \
                                 tokenizer = None,    \
                                 preprocessor = None, \
                                 stop_words = None,   \
                                 max_features = 5000) 
    
    all_ids,all_names,ids_turp,names_turp = extractmeta.collectallmeta()
    
    names_strings = []
    
    for names in names_turp:
        
        names_s = ""
        for name in names:
            #print name
            
            names_s = names_s + " " + str(unidecode(name))
                
            
        names_strings.append(names_s)
    
    
    vectorizer = CountVectorizer(analyzer = "word",   \
                                 tokenizer = None,    \
                                 preprocessor = None, \
                                 stop_words = None,   \
                                 max_features = 5000) 
    names_vec = vectorizer.fit_transform(names_strings)
    return names_vec
