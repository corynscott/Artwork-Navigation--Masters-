'''
Created on 15 Aug 2015

@author: Coryn
'''
import Tkinter as tk

from Tkinter import *
from PIL import ImageTk as ITk
from PIL import Image
from util import dirm, default_values
from databasehandler import imagesHandler
from features import interest_point_detectors
import cv2
from UI_matcher import matching

win = tk.Tk()

img1 = ITk.PhotoImage(Image.open(dirm.outputDirectory+"default.jpg"))
img1URL = 0
img2 = ITk.PhotoImage(Image.open(dirm.outputDirectory+"default.jpg"))
img2URL = 0
def searchImg(btId):
    
    imgURL = None
    if btId == 1:
        text = ent1.get().upper()
        try:
            imgURL = imagesHandler.get_full_url(text)
        except Exception,e:
            imgURL = None
            
        if imgURL == None:
            img1 = ITk.PhotoImage(Image.open(dirm.outputDirectory+"default.jpg"))
            img1URL = 0
        else:
            img1 = ITk.PhotoImage(Image.open(imgURL).resize((256,256),Image.ANTIALIAS))
            panel1.configure(image=img1)
            panel1.image = img1
            img1URL = imgURL
    if btId == 2:
        text = ent2.get().upper()
        
        try:
            imgURL = imagesHandler.get_full_url(text)
        except Exception,e:
            imgURL = None
            
        if imgURL == None:
            img2 = ITk.PhotoImage(Image.open(dirm.outputDirectory+"default.jpg"))
            img2URL = 0
        else:
            img2 = ITk.PhotoImage(Image.open(imgURL).resize((256,256),Image.ANTIALIAS))
            panel2.configure(image=img2)
            panel2.image = img2
            img2URL = imgURL
    
def match(crop_amount,ipd):
    out = None
    text1 = ent1.get().upper()
    text2 = ent2.get().upper()
    resize_ratio_m = float(ent3.get())
    print resize_ratio_m
    if resize_ratio_m == None:
        resize_ratio_m = default_values.resize_ratio
    num_matches = int(ent4.get())
    if num_matches == None:
        num_matches = 10
    print resize_ratio_m
    try:
        img1URL = imagesHandler.get_full_url(text1)
        img2URL = imagesHandler.get_full_url(text2)
        img1 = cv2.imread(img1URL)
        img2 = cv2.imread(img2URL)
        
        if ipd =="SURF":
            k1,d1,gray1 = interest_point_detectors.calculate_surf_values(img1,hessian_threshold=default_values.hessian_threshold,resize_ratio=resize_ratio_m,resize_method=default_values.resize_method,crop_amount=crop_amount)
            k2,d2,gray2 = interest_point_detectors.calculate_surf_values(img2,hessian_threshold=default_values.hessian_threshold,resize_ratio=resize_ratio_m,resize_method=default_values.resize_method,crop_amount=crop_amount)
        if ipd =="SIFT":
            k1,d1,gray1 = interest_point_detectors.calculate_sift_values(img1,resize_ratio=resize_ratio_m,resize_method=default_values.resize_method,crop_amount=crop_amount)
            k2,d2,gray2 = interest_point_detectors.calculate_sift_values(img2,resize_ratio=resize_ratio_m,resize_method=default_values.resize_method,crop_amount=crop_amount)
        if ipd =="ORB":
            k1,d1,gray1 = interest_point_detectors.calculate_orb_values(img1,resize_ratio=resize_ratio_m,resize_method=default_values.resize_method,crop_amount=crop_amount)
            k2,d2,gray2 = interest_point_detectors.calculate_orb_values(img2,resize_ratio=resize_ratio_m,resize_method=default_values.resize_method,crop_amount=crop_amount)
        
        
        out = matching.matchandDraw(gray1,gray2,k1,d1,k2,d2,num_matches)
    except Exception,e:
        print e
    return out

def save():
    text1 = ent1.get().upper()
    text2 = ent2.get().upper()
    out = match(crop_amount=default_values.crop_amount)
    cv2.imwrite(dirm.outputDirectory+"UI_matcher/" + text1 + "_match_" + text2+".jpg",out)
    

v1 = StringVar()
ent1 = tk.Entry(win,textvariable=v1)
ent1.pack()
v1.set("D24872")
ent1.grid(row=0,column=0)

v2 = StringVar()
ent2 = tk.Entry(win,textvariable=v2)
ent2.pack()
v2.set("D24871")
ent2.grid(row=1,column=0)

b1 = tk.Button(win,text="search")
b1.grid(row=0,column=1)
b1.configure(command= lambda: searchImg(1))

b2 = tk.Button(win,text="search")
b2.grid(row=1,column=1)
b2.configure(command= lambda: searchImg(2))

panel1 = tk.Label(win,image=img1)
panel1.grid(row=0,column=3)


panel2 = tk.Label(win,image=img1)
panel2.grid(row=1,column=3)


v3 = StringVar()
ent3 = tk.Entry(win,textvariable=v3,)
ent3.pack()
v3.set("0.4")
ent3.grid(row=2,column=0)


v4 = StringVar()
ent4 = tk.Entry(win,textvariable=v4)
ent4.pack()
v4.set("10")
ent4.grid(row=3,column=0)

listbox = Listbox(win)
listbox.pack()
listbox.grid(row=4,column=0)

items = ["SURF", "SIFT", "ORB"]
for item in items:
    listbox.insert(END, item)

listbox.activate(1)
item = listbox.curselection()
print item
    

b3 = tk.Button(win,text="Match", command = lambda: match(crop_amount=0,ipd=items[listbox.curselection()[0]]))
b3.grid(row=4,column=1)

b4 = tk.Button(win,text="Match Crop", command = lambda: match(crop_amount=100,ipd=items[listbox.curselection()[0]]))
b4.grid(row=4,column=2)
b4 = tk.Button(win,text="save", command = lambda: save())
b4.grid(row=4,column=3)

searchImg(1)
searchImg(2)

win.mainloop(   )

