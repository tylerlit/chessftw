import sys

import mysql.connector
from mysql.connector import Error

class dbConnection:
    #connection vars
    host = "chessftw.c51fcxedep9m.us-east-1.rds.amazonaws.com"
    database = "chess"
    user = "chessadmin"
    password = "chesspassword"

    def openConnection(self):
        try:
            self.connection = mysql.connector.connect(host = self.host,
                                                        database = self.database,
                                                        user = self.user,
                                                        password = self.password)
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as error:
            sys.exit("Failed to connect to mysql server: {}".format(error))
    
    def closeConnection(self):
        if (self.connection.is_connected()):
            self.cursor.close()
            self.connection.close()
        else:
            print("cannot close connection")

    def insert(self, _queryString, _args=None):
        try:
            result = self.cursor.execute(_queryString, _args)
            self.connection.commit()

        except mysql.connector.Error as error:
            sys.exit(" insert Failed to query database {}".format(error))

    def insertMany(self, _queryString, _args=None):
        try:
            result = self.cursor.executemany(_queryString, _args)
            self.connection.commit()

        except mysql.connector.Error as error:
            sys.exit(" insert Failed to query database {}".format(error))

    def select(self, _queryString, _args=None):
        try:
            self.cursor.execute(_queryString, _args)
            record = self.cursor.fetchall()
            return record
        except mysql.connector.Error as error:
            sys.exit("select Failed to query database {}".format(error))

    def delete(self, _queryString, _args=None):
        try:
            self.cursor.execute(_queryString, _args)
            self.connection.commit()
        except mysql.connector.Error as error:
            sys.exit("delete Failed to query database {}".format(error))