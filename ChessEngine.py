import chess
import random

board = chess.Board()

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def mateOpportunity(board):
    if (board.legal_moves.count() == 0):
        if board.turn == chess.WHITE:
            return -9999
        else:
            return 9999
    else:
        return 0

def squareResPoints(board, square):
    pieceValue = 0.0
    if board.piece_type_at(square) == chess.PAWN:
        pieceValue = 1.0
    elif board.piece_type_at(square) == chess.KNIGHT:
        pieceValue = 3.2
    elif board.piece_type_at(square) == chess.BISHOP:
        pieceValue = 3.33
    elif board.piece_type_at(square) == chess.ROOK:
        pieceValue = 5.1
    elif board.piece_type_at(square) == chess.QUEEN:
        pieceValue = 8.8
    return pieceValue

def opening(board):
    if (board.fullmove_number < 10):
        if board.turn == chess.BLACK:
            return 1/30 * board.legal_moves.count()
        else:
            return -1/30 * board.legal_moves.count()
    else:
        return 0

def get_all_set_bits(bits):
    bits_index = []
    for i, c in enumerate(bin(bits)[:1:-1], 1):
        if c == '1':
            bits_index.append(i-1)
    return bits_index

def evalFunc(board):
    compt = 0
    indices = get_all_set_bits(board.occupied)
    for i in indices:
        compt += squareResPoints(board, chess.SQUARES[i])
    compt += mateOpportunity(board) + opening(board) + 0.001 * random.random()
    for piece_type, value in piece_values.items():
        white_pieces = board.pieces(piece_type, chess.WHITE)
        black_pieces = board.pieces(piece_type, chess.BLACK)
        compt += (len(white_pieces) - len(black_pieces)) * value
    return compt

def getBestMove(board, depth):
    best_eval = float('-inf')
    best_move = None

    for move in board.legal_moves:
        board.push(move)
        evaluation = minimax(board, depth - 1, float('-inf'), float('inf'), False)
        board.pop()
        if evaluation > best_eval:
            best_eval = evaluation
            best_move = move

    return best_move

 
def minimax(board, depth, alpha, beta, maximizingPlayer):
    if (depth == 0 or board.is_game_over()):
        return evalFunc(board)
    
    if maximizingPlayer:
        maxEval = float("-inf")
        for i in board.legal_moves:
            board.push(i)
            evaluation = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float("inf")
        for i in board.legal_moves:
            board.push(i)
            evaluation = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return minEval







