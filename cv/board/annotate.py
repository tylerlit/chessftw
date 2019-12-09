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

class Annotate:

	def __init__(self, img, window, color):

		# create UI container
		root = tk.Tk()

		# make image larger for user's eyes
		piece = cv2.resize(img, None, fx=3, fy=3)

		# get window
		w = piece.shape[0] + 100 # get window width + 50 pixels for padding
		h = piece.shape[1] + 50 # and height 

		ws = root.winfo_screenwidth() # get width of the screen
		hs = root.winfo_screenheight() # and height of the screen

		# calculate window placement
		# new window
		if (window == (0, 0)):

			x = (ws/2) - (w/2)
			y = (hs/2) - (h/2)

		# keep old window placement
		else:

			# align window to position from before
			# i have no idea how to replace these values with constants
			x = window[0] - 12
			y = window[1] - 31

		# set window placement
		root.geometry('%dx%d+%d+%d' % (w, h, x, y))


		# create actual UI elements
		root = Window(master=root, img=piece, color=color)
	   
		# run it
		root.mainloop()

		self.window = root.window
		self.label = root.label

class Window(tk.Frame):

	# master: main window reference
	# img: image of chess piece to be displayed
	# color: color of chess piece (white/black)
	# window: location of window relative to screen
	def __init__(self, master=None, img=None, color=None, location=None):

		super().__init__(master)

		self.master = master
		self.location = location
		self.color = color
		self.labels = { 
						" rook ": "r", " bishop ": "b", " knight ": "n",
						" king ": "k", " queen ": "q", " pawn ": "p" 
						}

		# convert opencv image to PIL (Python Imaging Library?) format
		self.image = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
		self.image = Image.fromarray(self.image)
		self.image = ImageTk.PhotoImage(self.image)

		self.pack()
		self.create_widgets()

	# create UI elements
	def create_widgets(self):

		self.pieceImage = tk.Label(self, image=self.image).pack(side="top")

		for x, y in self.labels.items():
			button = tk.Button(self, text=x, command=lambda name=y: self.assignLabel(name))
			button.pack(side="left")\

	def assignLabel(self, label):

		self.label = label
		self.exit()

	def exit(self):

		if (self.color == "w"):
			self.label = self.label.upper()

		# save window for next annotation
		self.window = (self.winfo_rootx(), self.winfo_rooty())

		self.master.destroy()

def labelPieces(pieces):

	labels = []

	# keep location of window on screen to keep UI spawn consistent
	window = (0, 0)

	for piece in pieces:

		image = piece.copy()

		# get color
		color = getColor(piece)

		result = Annotate(image, window, color)

		window = result.window
		labels.append(result.label)
		print(result.label)

	return labels

def getColor(piece):

	piece = piece.copy()

	middle = getMiddle(piece)

	# filter color on average lightness
	color = round(np.mean(middle))

	if (color < 100):
		color = "b"
	else:
		color = "w"

	return color

def getMiddle(piece):  
	return piece[round(piece.shape[0] / 4):round(piece.shape[0] * (3/4)), 
				round(piece.shape[1] / 4):round(piece.shape[1] * (3/4))]

def getPieces(board):

	x = 0
	y = 0
	pieces = []

	board = board.copy()

	unit = round(board.shape[0] / 8)

	for k in range(8):

		for l in range(8):

			cell = board[unit * k:unit * (k+1), unit * l:unit * (l+1)]

			# get middle of cell where piece will always be (if present)
			middle = getMiddle(cell)

			# make darker pixels white in this area to isolate pieces
			middle = transform(middle)

			# filter pieces on average lightness of a space
			avg_color = round(np.mean(middle))

			# found a piece
			if (avg_color > 198):

				pieces.append(cell)

			x += unit

		x = 0
		y += unit

	return pieces

def getBoard(screenshot, og, cropxy):

	where = []
	img = screenshot.copy() 
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

	__MAX_RETURN_ROWS__ = 1
	temp_folder_path = './cv/board/temp/'
	root = '../..'

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
		id = i[:-4]
		y1 = dimensions[1][0]
		x1 = dimensions[0][0]
		y2 = dimensions[1][1]
		x2 = dimensions[1][0]

		# print("show crop from og image")
		# test = og[dimensions[0][1]:dimensions[1][1], dimensions[0][0]:dimensions[1][0]]
		# cv2.imshow("test", test)
		# cv2.waitKey(0)

		pieces = getPieces(board)

		print(f"found {len(pieces)} pieces")

		labels = labelPieces(pieces)

		files = []

		for j in pieces:

			file = str(uuid.uuid4()) + ".png"

			files.append(file)

		print(files)
		print(labels)
			# cv2.imwrite(file, piece)
			# pieces.append(file)


			# window, label = LabelPiece(piece, window)
			# # clean up 
			# os.remove(file)

