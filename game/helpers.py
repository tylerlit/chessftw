from constants import *

def initializeBoard(_board):
    #white pieces
    _board[FILE_A][RANK_1] = WHITE_ROOK
    _board[FILE_B][RANK_1] = WHITE_KNIGHT
    _board[FILE_C][RANK_1] = WHITE_BISHOP
    _board[FILE_D][RANK_1] = WHITE_QUEEN
    _board[FILE_E][RANK_1] = WHITE_KING
    _board[FILE_F][RANK_1] = WHITE_BISHOP
    _board[FILE_G][RANK_1] = WHITE_KNIGHT
    _board[FILE_H][RANK_1] = WHITE_ROOK

    _board[FILE_A][RANK_2] = WHITE_PAWN
    _board[FILE_B][RANK_2] = WHITE_PAWN
    _board[FILE_C][RANK_2] = WHITE_PAWN
    _board[FILE_D][RANK_2] = WHITE_PAWN
    _board[FILE_E][RANK_2] = WHITE_PAWN
    _board[FILE_F][RANK_2] = WHITE_PAWN
    _board[FILE_G][RANK_2] = WHITE_PAWN
    _board[FILE_H][RANK_2] = WHITE_PAWN

    #black pieces
    _board[FILE_A][RANK_8] = BLACK_ROOK
    _board[FILE_B][RANK_8] = BLACK_KNIGHT
    _board[FILE_C][RANK_8] = BLACK_BISHOP
    _board[FILE_D][RANK_8] = BLACK_QUEEN
    _board[FILE_E][RANK_8] = BLACK_KING
    _board[FILE_F][RANK_8] = BLACK_BISHOP
    _board[FILE_G][RANK_8] = BLACK_KNIGHT
    _board[FILE_H][RANK_8] = BLACK_ROOK

    _board[FILE_A][RANK_7] = BLACK_PAWN
    _board[FILE_B][RANK_7] = BLACK_PAWN
    _board[FILE_C][RANK_7] = BLACK_PAWN
    _board[FILE_D][RANK_7] = BLACK_PAWN
    _board[FILE_E][RANK_7] = BLACK_PAWN
    _board[FILE_F][RANK_7] = BLACK_PAWN
    _board[FILE_G][RANK_7] = BLACK_PAWN
    _board[FILE_H][RANK_7] = BLACK_PAWN

    #empty pieces
    for i in range(BOARD_SIZE):
        for j in range(RANK_3, RANK_7):
            _board[i][j] = EMPTY

# returns a dictionary for a given file and rank of a position
def position(_file, _rank):
    return {"FILE" : _file,
            "RANK" : _rank}

    