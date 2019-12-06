import cv2
import re
import math
import numpy as np
import os
import tkinter as tk
import uuid
from . import draw
from matplotlib import pyplot as plt
from PIL import Image, ImageTk
from s3 import S3_utils
from sql import mysqlutil as db

# UI class for annotating pieces
class Piece(tk.Frame):

    def __init__(self, master=None, img=None, color=None):

        super().__init__(master)

        self.master = master

        self.image = cv2.resize(img, None, fx=3, fy=3)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)
        self.image = Image.fromarray(self.image)
        self.image = ImageTk.PhotoImage(self.image)

        self.color = color

        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.img = tk.Label(self, image=self.image)
        self.img.pack(side="top")

        self.rook = tk.Button(self, text=" rook ", fg="red", command=self.addRook)
        self.rook.pack(side="left")

        self.bishop = tk.Button(self, text=" bishop ", fg="red", command=self.addBishop)
        self.bishop.pack(side="left")

        self.knight = tk.Button(self, text=" knight ", fg="red", command=self.addKnight)
        self.knight.pack(side="left")

        self.king = tk.Button(self, text=" king ", fg="red", command=self.addKing)
        self.king.pack(side="left")

        self.queen = tk.Button(self, text=" queen ", fg="red", command=self.addQueen)
        self.queen.pack(side="left")

        self.pawn= tk.Button(self, text=" pawn ", fg="red", command=self.addPawn)
        self.pawn.pack(side="left")

    def say_hi(self):
        print("hi there, everyone!")

    def addRook(self):

    	self.label = "r"
    	self.exit()

    def addBishop(self):

    	self.label = "b"
    	self.exit()

    def addKnight(self):

    	self.label = "n"
    	self.exit()

    def addKing(self):

    	self.label = "k"
    	self.exit()

    def addQueen(self):

    	self.label = "q"
    	self.exit()

    def addPawn(self):

    	self.label = "p"
    	self.exit()

    def exit(self):
    	print("exit")
    	if (self.color == "w"):
    		self.label = self.label.upper()

    	labels.append(self.label)

    	self.master.destroy()

def getBoard(image, og, cropxy):

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


def transform(image):
	img = image.copy()

	for y in range(image.shape[0]):

		for x in range(image.shape[1]):

			if img[y][x] < 100:
				img[y][x] = 255

	return img


def run():

    global __MAX_RETURN_ROWS__
    global temp_folder_path
    global root
    global labels

    __MAX_RETURN_ROWS__ = 1
    temp_folder_path = './cv/board/temp/'
    root = '../..'
    labels = []

    # query database for image paths that have not been annotated
    mydb = db.dbConnection()
    mydb.openConnection()
    cursor = mydb.cursor
    
    # call procedure which returns filepaths, and IDs which are not currently locked and not already annotated
    # also updates the locked flag before returning
    cursor.callproc("chess.getBoardImages", [__MAX_RETURN_ROWS__, ])
    results = cursor.stored_results()

    # parse eachresult set, and rows therein
    for result in results:

        for row in result:
            print(row)
            # save the file, naming it with its unique ID
            S3_utils.download_file('chessftw', row[1], temp_folder_path + str(row[0]) + '.png')


    # grab all files from ./cv/board/temp/
    files = [temp_folder_path + f for f in os.listdir(temp_folder_path) if os.path.isfile(temp_folder_path + f)]
    
    # get all screenshots from temp dir
    images = [i for i in files if (i[-4:] == ".png")]

    images = images[:1]

    for i in images:
        print("now processing " + i)

        img = cv2.imread(i, 0)
        og = img.copy()

        # draw cropped image and dimensions of crop relative to original image
        crop, cropxy = draw.draw(i)

        # convert result to grayscale
        img = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        # crop out background pixels that are not the board
        # also calculate starting x,y and ending x,y of board relative to original image
        board, dimensions = getBoard(img, og, cropxy)
        

        # data to upload
        id = i[-4:]
        y1 = dimensions[1][0]
        x1 = dimensions[0][0]
        y2 = dimensions[1][1]
        x2 = dimensions[1][0]

        # print("show crop from og image")
        # test = og[dimensions[0][1]:dimensions[1][1], dimensions[0][0]:dimensions[1][0]]
        # cv2.imshow("test", test)
        # cv2.waitKey(0)

        # img = cv2.resize(img, None ,fx=0.25,fy=0.25)
        # img = img[41:228, 143:329]
        
        # print(round(img.shape[0] / 8))
        # print(img[0,0])
        
        x = 0
        y = 0
        numPieces = 0

        pieces = []
        piece_avg = []
        
        copy = board.copy()
        unit = round(copy.shape[0] / 8)


        for k in range(8):

            for l in range(8):

                piece = copy[unit * k:unit * (k+1), unit * l:unit * (l+1)]
                middle = piece.copy()[round(piece.shape[0] / 4):round(piece.shape[0] * (3/4)), 
                					round(piece.shape[1] / 4):round(piece.shape[1] * (3/4))]

                # make darker pixels white to isolate pieces
                # spaces with pieces on the board are now lighter than empty spaces
                test = transform(middle)

                # filter on that
                avg_color = round(np.mean(test))
                piece_avg.append(avg_color)

                if (avg_color > 198):

                    # cv2.imshow("test", piece)
                    # cv2.waitKey(0)

                    file = str(uuid.uuid4()) + ".png"

                    color = round(np.mean(middle))

                    if (color < 100):
                    	color = "b"
                    else:
                    	color = "w"

                    numPieces += 1

                    cv2.imwrite(file, piece)


                    # annotate pieces
                    root = tk.Tk()

                    w = 800 # width for the Tk root
                    h = 650 # height for the Tk root

                    ws = root.winfo_screenwidth() # width of the screen
                    hs = root.winfo_screenheight() # height of the screen

					# calculate x and y coordinates for the Tk root window
                    x = (ws/2) - (w/2)
                    y = (hs/2) - (h/2)
                    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

                    root = Piece(master=root, img=piece, color=color)
                    root.mainloop()

                    pieces.append(file)

                    print(pieces)
                    print(labels)

                    os.remove(file)

                    # cv2.imshow("test", piece)
                    # cv2.waitKey(0)

                x += unit

            x = 0
            y += unit


        print(f"numPieces: {numPieces}")
        # img = img[:unit, :unit]
        
        # img.show(plot)



        # label = input("r k b q k p: ")