import pyscreenshot as ig
import uuid
import mysql.connector
from mysql.connector import Error


def insertBLOB(photo):
    print("Inserting BLOB into python_employee table")
    try:
        connection = mysql.connector.connect(host='chessftw.c51fcxedep9m.us-east-1.rds.amazonaws.com',
                                             database='chess',
                                             user='chessadmin',
                                             password='chesspassword')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO image
                          (image) VALUES (%s,%s)"""

        # Convert data into tuple format
        insert_blob_tuple = ("DEFAULT",photo)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


if __name__ == "__main__":
	img = ig.grab()
	img.save(str(uuid.uuid4()) + ".png")

	insertBLOB(img)
	

#img.show()