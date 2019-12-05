#!/usr/bin/env python
# coding: utf-8

# In[1]:
import os
import cv2

import re
import math
import tkinter as tk
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import tkinter as tk

from sql import mysqlutil as db
from s3 import S3_utils
from . import draw

def run():
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
    # query database for image paths that have not been annotated
    __MAX_RETURN_ROWS__ = 3
    mydb = db.dbConnection()
    mydb.openConnection()
    cursor = mydb.cursor

    #call procedure which returns filepaths, and IDs whichare not currently locked and not already annotated
    #also updates the locked flag before returning
    cursor.callproc('chess.getBoardImages', [__MAX_RETURN_ROWS__, ])
    results = cursor.stored_results()

    #setting path to telp folder
    temp_folder_path = './cv/board/temp/'

    # parse eachresult set, and rows therein
    for result in results:
        for row in result:
            #save the file, naming it with its unique ID
            S3_utils.download_file('chessftw',row[1],temp_folder_path + str(row[0]) + '.png')

    #grab all files from ./cv/board/temp/
    files = [temp_folder_path + f for f in os.listdir(temp_folder_path) if os.path.isfile(temp_folder_path + f)]

    # get all screenshots from temp dir
    images = [i for i in files if (i[-4:] == ".png")]
    # In[3]:
    for i in images:
        print('now processing ' + i)

        #TYLER I NEED YOU TO SHOW ME WHERE I SEND BACK THE ANNOTATION TO DATABASE
        #IDK HOW TO WORK YOUR UI
        img = cv2.imread(i, 0)
        og = img.copy()
        size = img.shape

        # draw cropped image and dimensions of crop relative to original image
        crop, cropxy = draw.draw(i)

        # convert result to grayscale
        img = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        # crop out background pixels that are not the board
        # also calculate starting x,y and ending x,y of board relative to original image
        board, dimensions = getBoard(img, og, cropxy, size)

        # print("show test")
        # test = og[dimensions[0][1]:dimensions[1][1], dimensions[0][0]:dimensions[1][0]]

        # cv2.imshow("test", test)
        # cv2.waitKey(0)

        # img = cv2.resize(img, None ,fx=0.25,fy=0.25)
        # img = img[41:228, 143:329]
        
        # print(round(img.shape[0] / 8))
        # print(img[0,0])
        
        y = 0
        x = 0
        unit = math.trunc(board.shape[0] / 8)
        middle = math.trunc(unit / 2)

        for j in range(8):

            for k in range(8):
                piece = board.copy()[y:unit * (j + 1), x:unit * (k + 1)]

                if piece[0][0] == piece[middle][middle]:
                    continue
                else:
                    cv2.imshow("test", piece)
                    cv2.waitKey(0)

                x += unit

            x = 0
            y += unit


        
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




