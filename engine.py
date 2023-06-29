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

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "  "
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.log.append(move)
        self.whiteTurn = not self.whiteTurn
        chess_board.push_san(move.getChessNotation())


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
        self.rank_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        self.row_ranks = {r: c for c, r in self.rank_rows.items()}

        self.file_columns = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        self.column_files = {r: c for c, r in self.file_columns.items()}

        self.piece_c = {"bR": "R", "bN": "N", "bB": "B", "bQ": "Q", "bK": "K", "bP": "", "wR": "R", "wN": "N", "wB": "B", "wQ": "Q", "wK": "K", "wP": "", "  ": "  "}
    
    def getChessNotation(self):
        self.checkCaptured(self.pieceMoved, self.pieceCaptured)
        if self.pawn_captured:
            string = self.getFile(self.startCol)
            return string + "x" + self.getRankFile(self.endRow, self.endCol)
        elif self.capturing:
            return self.getPieceMoved(self.pieceMoved) + "x" + self.getRankFile(self.endRow, self.endCol)
        else:
            return self.getPieceMoved(self.pieceMoved) + self.getRankFile(self.endRow, self.endCol)
    
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
