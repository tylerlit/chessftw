import pyscreenshot as ig
import uuid
import sql.mysqlutil as db
import cv.board.helpers as helpers

if __name__ == "__main__":
	#random file name
	savePath = str(uuid.uuid4()) + ".png"

	#open db connection
	mydb = db.dbConnection()
	mydb.openConnection()

	#get screenshopt and save temporarily
	img = ig.grab()
	img.save(savePath)

	#read the image file as binary
	binaryData = helpers.convertToBinaryData(savePath)

	#insert into the database
	mydb.insert("""INSERT INTO chess.image
				(id,image) VALUES (%s,%s)""", ("DEFAULT",binaryData))

	#retrieve image from db and write to file
	results = mydb.select("""SELECT id,image FROM chess.image
							ORDER BY id DESC LIMIT 1""")

	for row in results:
		fileName = "TEST_" + str(row[0]) + ".png"
		image = row[1]
		helpers.write_file(image,"cv\\board\\temp\\" + fileName)

	#close the connection
	mydb.closeConnection()

	#delete the original image file
	helpers.delete_file(savePath)