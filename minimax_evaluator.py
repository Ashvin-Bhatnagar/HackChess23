import chess

board = chess.Board()

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def evaluate_position(board):
    score = 0

    for piece_type, value in piece_values.items():
        white_pieces = board.pieces(piece_type, chess.WHITE)
        black_pieces = board.pieces(piece_type, chess.BLACK)
        score += (len(white_pieces) - len(black_pieces)) * value

    return score

def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_position(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, depth):
    best_eval = float('-inf')
    best_move = None

    for move in board.legal_moves:
        board.push(move)
        eval = minimax_alpha_beta(board, depth - 1, float('-inf'), float('inf'), False)
        board.pop()
        if eval > best_eval:
            best_eval = eval
            best_move = move

    return best_move

depth = 4

best_move = find_best_move(board, depth)
board.push(best_move)

print("Best Move:", best_move)
print("Position Evaluation:", evaluate_position(board))
print(board)