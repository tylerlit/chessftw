#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import draw
import re
import os
import tkinter as tk
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import tkinter as tk

#

# UI class for annotating pieces
class Piece(tk.Frame):
    def __init__(self, master=None, img=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self, image):
        self.hi_there = tk.Button(self)

        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

def getBoard(image, og, cropxy, size):

    where = []
    img = image.copy() 
    start = round(img.shape[0] / 2)
    beginning = 0
    counter = 0

    # check for the two colors of the board and crop out excess
    while (img[counter][start] < 100):
        counter += 1
    top = counter

    counter = beginning
    while (img[start][counter] < 100):
        counter += 1
    left = counter

    counter = img.shape[0] - 1
    while (img[counter][start] < 100):
        counter -= 1
    bottom = counter

    counter = img.shape[1] - 1
    while (img[start][counter] < 100):
        counter -= 1
    right = counter

    where.append((cropxy[0][0] + left, cropxy[0][1] + top))
    where.append((cropxy[1][0] - (img.shape[1] - right),
                cropxy[1][1] - (img.shape[0] - bottom)))

    board = img[top:bottom, left:right]

    return board, where

# In[2]:


# get all files in current directory (cv\board\)
files = [f for f in os.listdir('.') if os.path.isfile(f)]

# get all screenshots from current dir
images = [i for i in files if (i[-4:] == ".png")]

# print(files)
# print(images)


# In[3]:


for i in images:

    img = cv2.imread(i, 0)
    og = img.copy()
    size = img.shape

    # get cropped image and dimensions of crop relative to original image
    crop, cropxy = draw.draw(i)

    # convert to grayscale
    # theres probably a way more efficient alternative to this
    # but hey who cares amirite
    file = "test.jpg"
    cv2.imwrite(file, crop)
    img = cv2.imread(file, 0)

    copy = img.copy()

    # crop out background pixels that are not the board
    # also calculate starting x,y and ending x,y of board relative to original image
    board, dimensions = getBoard(img, og, cropxy, size)

    print("show test")
    test = og[dimensions[0][1]:dimensions[1][1], dimensions[0][0]:dimensions[1][0]]
    cv2.imshow("test", test)
    cv2.waitKey(0)

    # print(img)
    # print(img.shape)

    # img = cv2.resize(img, None ,fx=0.25,fy=0.25)
    # img = img[41:228, 143:329]
    
    #print(round(img.shape[0] / 8))
    #print(img[0,0])
    
    # unit = round(img.shape[0] / 8)
    
    # img = img[:unit, :unit]
    
    # img.show(plot)

    # # annotate pieces
    # root = tk.Tk()
    # app = Piece(master=root, image=img)
    # app.mainloop()

    # label = input("r k b q k p: ")

# In[ ]:







# In[ ]:





# In[ ]:





# In[ ]:




