import sys

from sql import mysqlutil as db
from s3 import S3_utils
def deleteBoardImage(id):
    """:param id: chess.board ID column

    function will delete the image in s3 and remove the row in the 
    chess.board table
    """

    #first get the s3 path from db
    mydb = db.dbConnection()
    mydb.openConnection()

    result = mydb.select("""SELECT 
                                Filepath
                            FROM
                                chess.board
                            WHERE
                                ID = %s""",(id,))

    s3Path = ""
    for row in result:
        s3Path = row[0]
    
    #delete the file from s3
    if S3_utils.delete_object('chessftw', s3Path) != True:
        mydb.closeConnection()
        sys.exit('unable to delete s3 object ' + s3Path)

    #now delete the row in chess.board
    mydb.delete("""DELETE
                    FROM
                        chess.board
                    WHERE
                        ID = %s""", (id,))
    mydb.closeConnection()

def dowloadBoards(path, max):
    """:param max: int, max number of file to download
        :param path: file path to download images to
        
        queries chess.board to get <max> number of file paths from s3,
        then downloads thos files from s3 to <path>"""

    #query the db
    mydb = db.dbConnection()
    mydb.openConnection()

    results = mydb.select("""SELECT 
                                Filepath, ID
                            FROM
                                chess.board
                            ORDER BY 
                                ID
                            LIMIT %s""", (int(max),))

    #for each row, call s3
    for row in results:
        filepath = path + str(row[1]) + '.png'
        S3_utils.download_file('chessftw', row[0], filepath)
        print(str(row[1]) + ' downloaded to ' + path)

    mydb.closeConnection()

def resetBoardLocks():
    mydb = db.dbConnection()
    mydb.openConnection()

    mydb.insert("""UPDATE chess.board
                    SET Locked = 0
                    WHERE ID <> 1""")
    mydb.closeConnection()

    



    
   