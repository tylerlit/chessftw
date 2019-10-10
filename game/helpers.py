import constants

def initializeBoard(_board):
    print("initializing game board")

    #white pieces
    _board[constants.FILE_A][constants.RANK_1] = constants.WHITE_ROOK
    _board[constants.FILE_B][constants.RANK_1] = constants.WHITE_KNIGHT
    _board[constants.FILE_C][constants.RANK_1] = constants.WHITE_BISHOP
    _board[constants.FILE_D][constants.RANK_1] = constants.WHITE_QUEEN
    _board[constants.FILE_E][constants.RANK_1] = constants.WHITE_KING
    _board[constants.FILE_F][constants.RANK_1] = constants.WHITE_BISHOP
    _board[constants.FILE_G][constants.RANK_1] = constants.WHITE_KNIGHT
    _board[constants.FILE_H][constants.RANK_1] = constants.WHITE_ROOK

    #black pieces
    _board[constants.FILE_A][constants.RANK_8] = constants.BLACK_ROOK
    _board[constants.FILE_B][constants.RANK_8] = constants.BLACK_KNIGHT
    _board[constants.FILE_C][constants.RANK_8] = constants.BLACK_BISHOP
    _board[constants.FILE_D][constants.RANK_8] = constants.BLACK_QUEEN
    _board[constants.FILE_E][constants.RANK_8] = constants.BLACK_KING
    _board[constants.FILE_F][constants.RANK_8] = constants.BLACK_BISHOP
    _board[constants.FILE_G][constants.RANK_8] = constants.BLACK_KNIGHT
    _board[constants.FILE_H][constants.RANK_8] = constants.BLACK_ROOK

    #empty pieces
    for i in range(8):
        for j in range(constants.RANK_2, constants.RANK_8):
            _board[i][j] = constants.EMPTY