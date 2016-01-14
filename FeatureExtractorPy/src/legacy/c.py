'''
Created on 23 Aug 2015

@author: Coryn
'''
from sklearn.feature_extraction.text import CountVectorizer
def dog(a,b,c):
    print "meta", a
    print "b", b 
    print "c", c
    
a = "dog"
b = ["cat","dog"]
if a == b[1]:
    print "here"
colours = [(255, 0, 0),(0, 0, 255),(0, 255, 0),(255, 0, 0),(255, 255, 0),(0, 255, 255),(255, 0, 255),(51, 25, 0),(0, 25, 51),(255,153,255)]
print len(colours)


vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000) 

a = ['dog cat dog','pig cat cat']
a = vectorizer.fit_transform(a)
print a.toarray()