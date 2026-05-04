import random

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.ai = 'O'
        self.human = 'X'
    
    def print_board(self):
        print()
        for i in range(3):
            print(f"  {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]}")
            if i < 2:
                print("  ---------")
        print()
    
    def is_win(self, player):
        b = self.board
        lines = [
            [b[0][0], b[0][1], b[0][2]], # Rows
            [b[1][0], b[1][1], b[1][2]],
            [b[2][0], b[2][1], b[2][2]],
            [b[0][0], b[1][0], b[2][0]], # Cols
            [b[0][1], b[1][1], b[2][1]],
            [b[0][2], b[1][2], b[2][2]],
            [b[0][0], b[1][1], b[2][2]], # Diagonals
            [b[0][2], b[1][1], b[2][0]]
        ]
        return [player, player, player] in lines
    
    def is_full(self):
        return all(cell != ' ' for row in self.board for cell in row)
    
    def get_available_moves(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ' ']
    
    def evaluate(self):
        if self.is_win(self.ai): return 1
        if self.is_win(self.human): return -1
        return 0

    def minimax(self, depth, alpha, beta, is_maximizing):
        score = self.evaluate()
        if score != 0 or self.is_full() or depth == 0:
            return score
            
        if is_maximizing:
            max_eval = -float('inf')
            for r, c in self.get_available_moves():
                self.board[r][c] = self.ai
                eval_score = self.minimax(depth - 1, alpha, beta, False)
                self.board[r][c] = ' '
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for r, c in self.get_available_moves():
                self.board[r][c] = self.human
                eval_score = self.minimax(depth - 1, alpha, beta, True)
                self.board[r][c] = ' '
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
            
    def get_ai_move(self):
        best_score = -float('inf')
        best_moves = []
        
        for r, c in self.get_available_moves():
            self.board[r][c] = self.ai
            score = self.minimax(9, -float('inf'), float('inf'), False)
            self.board[r][c] = ' '
            
            if score > best_score:
                best_score = score
                best_moves = [(r, c)]
            elif score == best_score:
                best_moves.append((r, c))
                
        # Randomize among the best moves to feel more natural and less robotic
        return random.choice(best_moves)
    
    def play(self):
        print("Tic-Tac-Toe (You: X, AI: O)")
        
        while True:
            self.print_board()
            
            # Human move
            while True:
                try:
                    user_input = input("Your move (row col): ")
                    row, col = map(int, user_input.split())
                    if not (0 <= row <= 2 and 0 <= col <= 2):
                        print("Please enter numbers between 0 and 2.")
                        continue
                    if self.board[row][col] != ' ':
                        print("Spot taken! Try again.")
                        continue
                    break
                except ValueError:
                    print("Invalid! Enter two numbers separated by a space (e.g., '1 1').")
            
            self.board[row][col] = self.human
            
            if self.is_win(self.human):
                self.print_board()
                print("You win! Great job!")
                break
            if self.is_full():
                self.print_board()
                print("It's a draw!")
                break
            
            # AI move
            print("AI is thinking...")
            row, col = self.get_ai_move()
            self.board[row][col] = self.ai
            print(f"AI placed at ({row}, {col})")
            
            if self.is_win(self.ai):
                self.print_board()
                print("AI wins! Better luck next time.")
                break
            if self.is_full():
                self.print_board()
                print("It's a draw!")
                break

if __name__ == "__main__":
    game = TicTacToe()
    game.play()
