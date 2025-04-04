def minimax_alpha_beta(board, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    elif '_' not in [cell for row in board for cell in row]:
        return 0
    
    if is_maximizing:
        best_score = float('-inf')
        for move in get_empty_cells(board):
            board[move[0]][move[1]] = 'X'
            score = minimax_alpha_beta(board, False, alpha, beta)
            board[move[0]][move[1]] = '_'
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # Beta cutoff
        return best_score
    else:
        best_score = float('inf')
        for move in get_empty_cells(board):
            board[move[0]][move[1]] = 'O'
            score = minimax_alpha_beta(board, True, alpha, beta)
            board[move[0]][move[1]] = '_'
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # Alpha cutoff
        return best_score

def ai_move_alpha_beta(board):
    best_score = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    for move in get_empty_cells(board):
        board[move[0]][move[1]] = 'X'
        score = minimax_alpha_beta(board, False, alpha, beta)
        board[move[0]][move[1]] = '_'
        if score > best_score:
            best_score = score
            best_move = move
    board[best_move[0]][best_move[1]] = 'X'
    print("AI's move:")
    print_board(board)# Codesoft
