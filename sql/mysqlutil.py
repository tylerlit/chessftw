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
            print("Failed to connect to mysql server: {}".format(error))
    
    def closeConnection(self):
        if (self.connection.is_connected()):
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")
        else:
            print("cannot close connection")

    def insert(self, _queryString, _args=None):
        try:
            result = self.cursor.execute(_queryString, _args)
            self.connection.commit()

        except mysql.connector.Error as error:
            print("Failed to query database {}".format(error))

    def select(self, _queryString, _args=None):
        try:
            self.cursor.execute(_queryString, _args)
            record = self.cursor.fetchall()
            return record
        except mysql.connector.Error as error:
            print("Failed to query database {}".format(error))