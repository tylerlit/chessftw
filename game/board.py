import constants
import helpers

class Board:
    board = [[constants.EMPTY for i in range(8)] for i in range(8)]

    def __init__(self):
        helpers.initializeBoard(self.board)

    def getBoardString(self):
        retStr = ""
        for i in reversed(range(8)):
            for j in range(8):
                retStr = retStr + self.board[j][i] + " "
            retStr = retStr + "\n"
        return retStr

    #def makeMove(self, color, move):
