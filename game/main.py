from board import Board
from helpers import position
from constants import *

myBoard = Board()

myBoard.movePiece(WHITE_PAWN, position(FILE_E,RANK_2), position(FILE_E,RANK_4))
myBoard.movePiece(BLACK_PAWN, position(FILE_E,RANK_7), position(FILE_E,RANK_5))



print(myBoard.getBoardString())


