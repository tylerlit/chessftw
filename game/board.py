from constants import *
from helpers import *

class Board:
    board = [[EMPTY for i in range(8)] for i in range(8)]

    def __init__(self):
        initializeBoard(self.board)

    def getBoardString(self):
        retStr = ""
        for i in reversed(range(8)):
            for j in range(8):
                retStr = retStr + self.board[j][i] + " "
            retStr = retStr + "\n"
        return retStr

    def movePiece(self, _piece, _from, _to):
        #make the previous space blank
        self.board[_from["FILE"]][_from["RANK"]] = EMPTY

        #fill the new spot with the given piece
        self.board[_to["FILE"]][_to["RANK"]] = _piece
