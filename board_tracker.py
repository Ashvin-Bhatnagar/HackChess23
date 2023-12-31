import numpy as np
import chess
from stockfish import Stockfish

stockfish = Stockfish()


chess_board = chess.Board()
'''
stockfish.set_fen_position(chess_board.fen())

print(stockfish.get_best_move())
'''

rank_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
row_ranks = {r: c for c, r in rank_rows.items()}

file_columns = {"a": 0, "b": 1, "c": 2,
                             "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
column_files = {r: c for c, r in file_columns.items()}


class State():
    def __init__(self):
        # Board
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])

        self.whiteTurn = True
        self.log = []
        self.won = False
        self.draw = False
        self.enpassantPossible = ()
        self.piece_c = {"bR": "R", "bN": "N", "bB": "B", "bQ": "Q", "bK": "K", "bP": "",
                        "wR": "R", "wN": "N", "wB": "B", "wQ": "Q", "wK": "K", "wP": "", "  ": "  "}
        self.b_p_pieces = {"Q": "bQ", "R": "bR", "B": "bB", "N": "bN"}
        self.promoted_to = ""
        self.wants_to_move = ""
        self.valid_promotion = False
        self.isEnpassantPossible = False
        self.black_king_castle = False
        self.black_queen_castle = False

    def makeWhiteMove(self, move):
        move.is_castle()
        move.is_promotion()
        move.en_passant()

        self.board[move.startRow][move.startCol] = "  "
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.log.append(move)
        


        if self.whiteTurn:
            if move.valid_promotion:
                if self.whiteTurn:
                    self.board[move.endRow][move.endCol] = move.w_p_pieces[move.promoted_to]

            if move.isEnpassantPossible:
                self.board[move.startRow][move.endCol] = "  "

            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = (
                    (move.startRow + move.endRow) // 2, move.endCol)
            else:
                self.enpassantPossible = ()

            if move.white_king_castle:
                if chess_board.has_kingside_castling_rights(chess.WHITE):
                    self.board[7][7] = "  "
                    self.board[7][5] = "wR"
                else:
                    self.valid = False

            elif move.white_queen_castle:
                if chess_board.has_queenside_castling_rights(chess.WHITE):
                    self.board[7][0] = "  "
                    self.board[7][3] = "wR"
                else:
                    self.valid = False


            self.whiteTurn = not self.whiteTurn
            chess_board.push_san(move.getStandardChessNotation())

            if chess_board.is_checkmate():
                self.won = True
            if chess_board.is_stalemate() or chess_board.is_insufficient_material() or chess_board.can_claim_threefold_repetition() or chess_board.can_claim_fifty_moves() or chess_board.can_claim_draw() or chess_board.is_fivefold_repetition() or chess_board.is_seventyfive_moves():
                self.draw = True
    
    def makeBlackMove(self):
        if not self.whiteTurn and not chess_board.is_checkmate():
            self.is_castle()
            self.is_promotion()
            self.en_passant()
            
            stockfish.set_fen_position(chess_board.fen())
            self.best_move = stockfish.get_best_move()
            print(self.best_move)
            self.start_col = file_columns[self.best_move[0]]
            self.start_row = rank_rows[self.best_move[1]]
            self.end_col = file_columns[self.best_move[2]]
            self.end_row = rank_rows[self.best_move[3]]
            self.wants_to_move = self.board[self.start_row][self.start_col]
            self.valid_promotion = False
            self.isEnpassantPossible = False
            self.black_king_castle = False
            self.black_queen_castle = False

            self.board[self.start_row][self.start_col] = "  "
            self.board[self.end_row][self.end_col] = self.wants_to_move

            if self.valid_promotion:
                self.board[self.end_row][self.end_col] = self.b_p_pieces[self.promoted_to]

            if self.isEnpassantPossible:
                self.board[self.start_row][self.end_col] = "  "

            if self.wants_to_move[1] == 'p' and abs(self.start_row - self.end_row) == 2:
                self.enpassantPossible = (
                    (self.start_row + self.end_row) // 2, self.end_col)
            else:
                self.enpassantPossible = ()

            if self.best_move == "e8g8":
                if chess_board.has_kingside_castling_rights(chess.BLACK):
                    self.board[0][7] = "  "
                    self.board[0][5] = "bR"

            elif self.best_move == "e8c8":
                if chess_board.has_queenside_castling_rights(chess.BLACK):
                    self.board[0][0] = "  "
                    self.board[0][3] = "bR"
                else:
                    self.valid = False


            self.whiteTurn = not self.whiteTurn
            chess_board.push_san(self.best_move)

            if chess_board.is_checkmate():
                self.won = True
            if chess_board.is_stalemate() or chess_board.is_insufficient_material() or chess_board.can_claim_threefold_repetition() or chess_board.can_claim_fifty_moves() or chess_board.can_claim_draw() or chess_board.is_fivefold_repetition() or chess_board.is_seventyfive_moves():
                self.draw = True

    def is_promotion(self):
        if (self.wants_to_move == "wP" and self.start_row == 1):
            if self.end_row == 0:
                self.valid_promotion = True
            else:
                self.valid_promotion = False
        if (self.wants_to_move == "bP" and self.start_row == 6):
            if self.end_row == 7:
                self.valid_promotion = True
            else:
                self.valid_promotion = False

    def en_passant(self):
        if self.wants_to_move == "wP":
            if self.start_row == 3 and self.end_row == 2:
                if self.board[self.start_row][self.end_col] == "bP":
                    self.isEnpassantPossible = True

        elif self.wants_to_move == "bP":
            if self.start_row == 4 and self.end_row == 5:
                if self.board[self.start_row][self.end_col] == "wP":
                    self.isEnpassantPossible = True




class Move():

    def __init__(self, startSQ, endSQ, board, enpassantPossible=False):
        self.bd = board
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.capturing = False
        self.pawn_captured = False

        self.piece_c = {"bR": "R", "bN": "N", "bB": "B", "bQ": "Q", "bK": "K", "bP": "",
                        "wR": "R", "wN": "N", "wB": "B", "wQ": "Q", "wK": "K", "wP": "", "  ": "  "}
        self.w_p_pieces = {"Q": "wQ", "R": "wR", "B": "wB", "N": "wN"}
        self.b_p_pieces = {"Q": "bQ", "R": "bR", "B": "bB", "N": "bN"}

        self.white_king_castle = False
        self.white_queen_castle = False
        self.black_king_castle = False
        self.black_queen_castle = False
        self.valid_promotion = False
        self.promoted_to = ""
        self.is_w_en_passant = False
        self.is_b_en_passant = False
        self.to_square = self.bd[self.endRow][self.endCol]

        self.isEnpassantPossible = enpassantPossible

    def getStandardChessNotation(self):
        self.checkCaptured(self.pieceMoved, self.pieceCaptured)
        self.is_castle()
        self.is_promotion()
        if self.valid_promotion:
            if self.pawn_captured:
                return self.getFile(self.startCol) + "x" + self.getRankFile(self.endRow, self.endCol) + self.promoted_to
            else:
                return self.getRankFile(self.endRow, self.endCol) + self.promoted_to
        else:
            if self.white_king_castle:
                return "0-0"
            elif self.white_queen_castle:
                return "0-0-0"
            elif self.black_king_castle:
                return "0-0"
            elif self.black_queen_castle:
                return "0-0-0"
            else:
                if self.pawn_captured:
                    string = self.getFile(self.startCol)
                    return string + "x" + self.getRankFile(self.endRow, self.endCol)
                elif self.capturing:
                    return self.getPieceMoved(self.pieceMoved) + "x" + self.getRankFile(self.endRow, self.endCol)
                else:
                    return self.getPieceMoved(self.pieceMoved) + self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def checkCaptured(self, start, end):
        if (self.getPieceMoved(start) == "" or self.getPieceMoved(start) == "") and (self.getPieceCaptured(end) != "  "):
            self.pawn_captured = True
        elif self.getPieceCaptured(end) != "  ":
            self.capturing = True

    def getRankFile(self, r, c):
        return column_files[c] + row_ranks[r]

    def getPieceMoved(self, pm):
        return self.piece_c[pm]

    def getFile(self, c):
        return column_files[c]

    def getPiece(self, r, c):
        return self.bd[r][c]

    def getPieceCaptured(self, pc):
        return self.piece_c[pc]

    def is_castle(self):
        if (self.pieceMoved == "wK"):
            if (self.endCol == 6 and self.endRow == 7):
                self.white_king_castle = True
            elif (self.endCol == 2 and self.endRow == 7):
                self.white_queen_castle = True
        elif (self.pieceMoved == "bK"):
            if (self.endCol == 6 and self.endRow == 0):
                self.black_king_castle = True
            elif (self.endCol == 2 and self.endRow == 0):
                self.black_queen_castle = True

    def is_promotion(self):
        if (self.pieceMoved == "wP" and self.startRow == 1):
            if self.endRow == 0:
                self.valid_promotion = True
            else:
                self.valid_promotion = False
        if (self.pieceMoved == "bP" and self.startRow == 6):
            if self.endRow == 7:
                self.valid_promotion = True
            else:
                self.valid_promotion = False

    def en_passant(self):
        if self.pieceMoved == "wP":
            if self.startRow == 3 and self.endRow == 2:
                if self.bd[self.startRow][self.endCol] == "bP":
                    self.isEnpassantPossible = True

        elif self.pieceMoved == "bP":
            if self.startRow == 4 and self.endRow == 5:
                if self.bd[self.startRow][self.endCol] == "wP":
                    self.isEnpassantPossible = True
