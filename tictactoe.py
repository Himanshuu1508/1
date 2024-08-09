import math

def initialize_board():
    return [' ' for _ in range(9)]

def print_board(board):
    for row in [board[i:i+3] for i in range(0, len(board), 3)]:
        print('| ' + ' | '.join(row) + ' |')

def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6]              
    ]
    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

def is_board_full(board):
    return ' ' not in board

def get_available_moves(board):
    return [i for i in range(len(board)) if board[i] == ' ']

def make_move(board, index, player):
    board[index] = player

def undo_move(board, index):
    board[index] = ' '

def minimax(board, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
    if check_winner(board, 'X'):
        return -1  
    elif check_winner(board, 'O'):
        return 1  
    elif is_board_full(board):
        return 0  

    if is_maximizing:
        max_eval = -math.inf
        for move in get_available_moves(board):
            make_move(board, move, 'O')
            eval = minimax(board, depth + 1, False, alpha, beta)
            undo_move(board, move)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in get_available_moves(board):
            make_move(board, move, 'X')
            eval = minimax(board, depth + 1, True, alpha, beta)
            undo_move(board, move)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board):
    best_score = -math.inf
    best_move = None
    for move in get_available_moves(board):
        make_move(board, move, 'O')
        score = minimax(board, 0, False)
        undo_move(board, move)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def play_game():
    board = initialize_board()
    print("Welcome to Tic-Tac-Toe!")
    print("You are 'X' and the AI is 'O'.")
    
    while True:
        print_board(board)
        
        move = int(input("Enter your move (1-9): ")) - 1
        if board[move] != ' ':
            print("Invalid move. Try again.")
            continue
        make_move(board, move, 'X')
        
        if check_winner(board, 'X'):
            print_board(board)
            print("Congratulations! You win!")
            break
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        
        print("AI is making a move...")
        ai_move = find_best_move(board)
        make_move(board, ai_move, 'O')
        
        if check_winner(board, 'O'):
            print_board(board)
            print("AI wins! Better luck next time.")
            break
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

if __name__ == "__main__":
    play_game()
