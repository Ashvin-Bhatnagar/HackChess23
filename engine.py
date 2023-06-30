import numpy as np
import chess

chess_board = chess.Board()


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

    def makeMove(self, move):
        move.is_castle()
        move.is_promotion()

        if move.valid_promotion:
            self.board[move.startRow][move.startCol] = "  "
            if self.whiteTurn:
                self.board[move.endRow][move.endCol] = move.w_p_pieces[move.promoted_to]
                self.log.append(move)
                self.whiteTurn = not self.whiteTurn
                chess_board.push_san(move.getChessNotation())
            else:
                self.board[move.endRow][move.endCol] = move.b_p_pieces[move.promoted_to]
                self.log.append(move)
                self.whiteTurn = not self.whiteTurn
                chess_board.push_san(move.getChessNotation())
        else:
            if move.white_king_castle:
                if not chess_board.has_kingside_castling_rights(chess.WHITE):
                    self.valid = False
                else:
                    self.board[move.startRow][move.startCol] = "  "
                    self.board[move.endRow][move.endCol] = move.pieceMoved
                    self.board[7][7] = "  "
                    self.board[7][5] = "wR"
                    self.log.append(move)
                    self.whiteTurn = not self.whiteTurn
                    chess_board.push_san(move.getChessNotation())
            elif move.white_queen_castle:
                if not chess_board.has_queenside_castling_rights(chess.WHITE):
                    self.valid = False
                else:
                    self.board[move.startRow][move.startCol] = "  "
                    self.board[move.endRow][move.endCol] = move.pieceMoved
                    self.board[7][0] = "  "
                    self.board[7][3] = "wR"
                    self.log.append(move)
                    self.whiteTurn = not self.whiteTurn
                    chess_board.push_san(move.getChessNotation())
            elif move.black_king_castle:
                if not chess_board.has_kingside_castling_rights(chess.BLACK):
                    self.valid = False
                else:
                    self.board[move.startRow][move.startCol] = "  "
                    self.board[move.endRow][move.endCol] = move.pieceMoved
                    self.board[0][7] = "  "
                    self.board[0][5] = "bR"
                    self.log.append(move)
                    self.whiteTurn = not self.whiteTurn
                    chess_board.push_san(move.getChessNotation())
            elif move.black_queen_castle:
                if not chess_board.has_queenside_castling_rights(chess.BLACK):
                    self.valid = False
                else:
                    self.board[move.startRow][move.startCol] = "  "
                    self.board[move.endRow][move.endCol] = move.pieceMoved
                    self.board[0][0] = "  "
                    self.board[0][3] = "bR"
                    self.log.append(move)
                    self.whiteTurn = not self.whiteTurn
                    chess_board.push_san(move.getChessNotation())
            else:
                self.board[move.startRow][move.startCol] = "  "
                self.board[move.endRow][move.endCol] = move.pieceMoved
                self.log.append(move)
                self.whiteTurn = not self.whiteTurn
                chess_board.push_san(move.getChessNotation())

        if chess_board.is_checkmate():
            self.won = True
        if chess_board.is_stalemate() or chess_board.is_insufficient_material() or chess_board.can_claim_threefold_repetition() or chess_board.can_claim_fifty_moves() or chess_board.can_claim_draw() or chess_board.is_fivefold_repetition() or chess_board.is_seventyfive_moves():
            self.draw = True


'''
    def undoMove(self):
        if len(self.log) != 0:
            last = self.log.pop()
            self.board[last.startRow][last.startCol] = last.pieceMoved
            self.board[last.endRow][last.endCol] = last.pieceCaptured
            self.whiteTurn = not self.whiteTurn
            chess_board.pop()
'''


class Move():

    def __init__(self, startSQ, endSQ, board):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.capturing = False
        self.pawn_captured = False
        self.rank_rows = {"1": 7, "2": 6, "3": 5,
                          "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        self.row_ranks = {r: c for c, r in self.rank_rows.items()}

        self.file_columns = {"a": 0, "b": 1, "c": 2,
                             "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        self.column_files = {r: c for c, r in self.file_columns.items()}

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

    def getChessNotation(self):
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
        return self.column_files[c] + self.row_ranks[r]

    def getPieceMoved(self, pm):
        return self.piece_c[pm]

    def getFile(self, c):
        return self.column_files[c]

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
