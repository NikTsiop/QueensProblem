#!/qp_env/Scripts/python.exe
import random
import matplotlib.pyplot as plt

class NQueens:
    
    success_times = 0
    lateral_steps_limit = 0
    
    def __init__(self, size):
        self.size = size
        self.board = [-1] * size
        self.moves_made = 0
        self.threats = 0

    def initialize(self, random_place):
        """Randomly place queens on the board or all the queens in the bottom"""
        if random_place:
            for col in range(self.size):
                self.board[col] = random.randint(0, self.size - 1)
        else:
            for col in range(self.size):
                self.board[col] = self.size-1

    def calculate_threats(self):
        """Calculate the number of threats."""
        threats = 0
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if self.board[i] == self.board[j] or \
                   abs(self.board[i] - self.board[j]) == j - i:
                    threats += 1
        return threats

    def hill_climbing(self, max_iterations):
        """Hill climbing algorithm."""
        current_threats = self.calculate_threats()
        for _ in range(max_iterations):
            moves = []
            for i in range(self.size):
                for j in range(self.size):
                    if j != self.board[i]:
                        # Calculate threats if we move the queen
                        original_value = self.board[i]
                        self.board[i] = j
                        new_threats = self.calculate_threats()
                        if new_threats < current_threats:
                            moves.append((i, j, new_threats))
                        self.board[i] = original_value

            if not moves:
                break

            # Make the best move
            best_move = min(moves, key=lambda x: x[2])
            self.board[best_move[0]] = best_move[1]
            current_threats = best_move[2]
            self.moves_made += 1
            self.threats = current_threats

    def hill_climbing_lateral_steps(self, max_iterations):
        """Hill climbing algorithm with lateral steps."""
        current_threats = self.calculate_threats()
        for _ in range(max_iterations):
            moves = []
            lateral_steps = 0
            for i in range(self.size):
                for j in range(self.size):
                    if j != self.board[i]:
                        # Calculate threats if we move the queen
                        original_value = self.board[i]
                        self.board[i] = j
                        new_threats = self.calculate_threats()
                        if new_threats < current_threats or \
                            (new_threats == current_threats and lateral_steps < self.lateral_steps_limit):
                            if new_threats == current_threats:
                                lateral_steps += 1
                            moves.append((i, j, new_threats))
                        self.board[i] = original_value

            if not moves:
                break

            # Make the best move
            best_move = min(moves, key=lambda x: x[2])
            self.board[best_move[0]] = best_move[1]
            current_threats = best_move[2]
            self.moves_made += 1
            self.threats = current_threats

    def display(self, stats=True):
        """Display the board by column."""
        print('_________')
        for col in range(self.size):
            line = []
            for row in range(self.size):
                if self.board[row] == col:
                    line.append('Q')
                else:
                    line.append('.')
            print(' '.join(line))
        if stats:
            if(self.threats == 0):
                self.success_times += 1
            print(f"Moves made: {self.moves_made}")
            print(f"Threats: {self.threats}")

def create_bar_graph(categories, values):
    plt.bar(categories, values)
    plt.title('N-Queens Problem')
    plt.xlabel('Categories')
    plt.ylabel('Success rate %')
    plt.show()

if __name__ == "__main__":
    size = 4
    nqueens = NQueens(size)
    repetitions = 100
    nqueens.lateral_steps_limit = 2
    random_queen_placement = True
    max_search_repetitions = 100
    
    categories = ['Hill climbing','Hill climbing + lateral steps']
    success_rates = []
    
    print('Using Hill climbing')
    for i in range(repetitions):
        nqueens.moves_made = 0
        nqueens.threats = 0
        
        nqueens.initialize(random_queen_placement)
        print('Start state')
        nqueens.display(False)
        nqueens.hill_climbing(max_search_repetitions)
        print('Final state')
        nqueens.display()    
        
    success_rates.append((nqueens.success_times/repetitions)*100)
    
    nqueens.success_times = 0
    
    print('Using Hill climbing with lateral steps')
    for i in range(repetitions):
        nqueens.moves_made = 0
        nqueens.threats = 0
        
        nqueens.initialize(random_queen_placement)
        print('Start state')
        nqueens.display(False)
        nqueens.hill_climbing_lateral_steps(max_search_repetitions)
        print('Final state')
        nqueens.display()
        
    success_rates.append((nqueens.success_times/repetitions)*100)
    
    # show statistics    
    create_bar_graph(categories, success_rates)