import time
import random
from math import inf

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.human_player = 'X'
        self.ai_player = 'O'
        self.winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), 
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  
            (0, 4, 8), (2, 4, 6)           
        ]
        self.nodes_evaluated = 0
        self.difficulty = 'hard'  

    def print_board(self):
        print("\n")
        print(f" {self.board[0]} │ {self.board[1]} │ {self.board[2]} ")
        print("───┼───┼───")
        print(f" {self.board[3]} │ {self.board[4]} │ {self.board[5]} ")
        print("───┼───┼───")
        print(f" {self.board[6]} │ {self.board[7]} │ {self.board[8]} ")
        print("\n")

    def is_valid_move(self, move):
        """Check if a move is valid"""
        return 0 <= move < 9 and self.board[move] == ' '

    def make_move(self, move):
        """Make a move on the board"""
        if self.is_valid_move(move):
            self.board[move] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def undo_move(self, move):
        """Undo a move (for AI simulation)"""
        self.board[move] = ' '
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_win(self):
        """Check if the current board state has a winner"""
        for a, b, c in self.winning_combinations:
            if self.board[a] != ' ' and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def is_board_full(self):
        """Check if the board is full (tie)"""
        return ' ' not in self.board

    def evaluate_board(self):
        """Evaluate the board state for the AI"""
        winner = self.check_win()
        if winner == self.ai_player:
            return 10
        elif winner == self.human_player:
            return -10
        else:
             score = 0
        for combo in self.winning_combinations:
                values = [self.board[i] for i in combo]
                ai_count = values.count(self.ai_player)
                human_count = values.count(self.human_player)
                
                if ai_count == 2 and human_count == 0:
                    score += 5
                elif ai_count == 1 and human_count == 0:
                    score += 1
                elif human_count == 2 and ai_count == 0:
                    score -= 5
                elif human_count == 1 and ai_count == 0:
                    score -= 1
        return score

    def minimax(self, depth, is_maximizing, alpha=-inf, beta=inf):
        """Minimax algorithm with alpha-beta pruning"""
        self.nodes_evaluated += 1
        
        winner = self.check_win()
        if winner == self.ai_player:
            return 10 - depth
        elif winner == self.human_player:
            return -10 + depth
        elif self.is_board_full():
            return 0

        if is_maximizing:
            best_score = -inf
            for i in range(9):
                if self.is_valid_move(i):
                    self.make_move(i)
                    score = self.minimax(depth + 1, False, alpha, beta)
                    self.undo_move(i)
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = inf
            for i in range(9):
                if self.is_valid_move(i):
                    self.make_move(i)
                    score = self.minimax(depth + 1, True, alpha, beta)
                    self.undo_move(i)
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
            return best_score

    def get_best_move(self):
        """Determine the best move using minimax with alpha-beta pruning"""
        best_score = -inf
        best_move = -1
        equal_moves = []
        
        
        max_depth = {
            'easy': 2,
            'medium': 4,
            'hard': 8
        }.get(self.difficulty, 8)

        start_time = time.time()
        self.nodes_evaluated = 0

        for i in range(9):
            if self.is_valid_move(i):
                self.make_move(i)
                score = self.minimax(0, False, -inf, inf)
                self.undo_move(i)
                
                if score > best_score:
                    best_score = score
                    best_move = i
                    equal_moves = [i]
                elif score == best_score:
                    equal_moves.append(i)

        if equal_moves:
            best_move = random.choice(equal_moves)

        elapsed_time = time.time() - start_time
        print(f"AI evaluated {self.nodes_evaluated} nodes in {elapsed_time:.2f} seconds")
        
        return best_move

    def set_difficulty(self):
        """Let the player choose the difficulty level"""
        print("\nChoose difficulty level:")
        print("1 - Easy")
        print("2 - Medium")
        print("3 - Hard")
        choice = input("Enter your choice (1-3): ")
        self.difficulty = ['easy', 'medium', 'hard'][int(choice)-1] if choice in ['1', '2', '3'] else 'hard'
        print(f"\nDifficulty set to {self.difficulty.upper()}")

    def choose_player(self):
        """Let the player choose X or O"""
        choice = input("Do you want to play as X or O? (X goes first) ").upper()
        if choice == 'O':
            self.human_player = 'O'
            self.ai_player = 'X'
        else:
            print("Defaulting to X")

    def play(self):
        """Main game loop"""
        print("Welcome to Advanced Tic-Tac-Toe!")
        self.choose_player()
        self.set_difficulty()

        while True:
            self.print_board()

            if self.current_player == self.human_player:
                move = input(f"Player {self.current_player}, enter your move (1-9): ")
                try:
                    move = int(move) - 1
                    if not self.make_move(move):
                        print("Invalid move. Try again.")
                        continue
                except ValueError:
                    print("Please enter a number between 1 and 9.")
                    continue
            else:
                print(f"AI ({self.ai_player}) is thinking...")
                move = self.get_best_move()
                self.make_move(move)
                print(f"AI plays at position {move + 1}")

            winner = self.check_win()
            if winner:
                self.print_board()
                if winner == self.human_player:
                    print("Congratulations! You win!")
                else:
                    print("AI wins!")
                break
            elif self.is_board_full():
                self.print_board()
                print("It's a tie!")
                break

        play_again = input("Would you like to play again? (y/n): ").lower()
        if play_again == 'y':
            self.__init__()
            self.play()
        else:
            print("Thanks for playing!")

if __name__ == "__main__":
    game = TicTacToe()
    game.play()