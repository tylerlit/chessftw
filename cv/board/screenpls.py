import pyscreenshot as ig
import uuid
import os
import sys
from s3 import S3_utils
from sql import mysqlutil as db

if __name__ == "__main__":

	#random file name
	fileName = str(uuid.uuid4()) + ".png"
	savePath = "cv/board/temp/" + fileName

	#get screenshopt and save temporarily
	img = ig.grab()
	img.save(savePath)

	#store in S3
	S3objectName = 'board/' + fileName
	if S3_utils.upload_file(savePath,'chessftw',S3objectName) :
		print('screenshot uploaded to S3 successfully!')
	else:
		sys.exit('screenshot failed to upload to S3')
	
	#store file path in DB
	mydb = db.dbConnection()
	mydb.openConnection()

	mydb.insert("""INSERT INTO chess.board
				(ID,Filepath) VALUES (%s,%s)""", ("DEFAULT",S3objectName))

	#clean up, close connection, delete the image file
	mydb.closeConnection()
	os.remove(savePath)

	

