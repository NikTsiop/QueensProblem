#!/qp_env/Scripts/python.exe
import numpy as np
import random as rd
import logging

#logger
logging.basicConfig(filename="logs.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Threat range DL,DR : down left/righ diagonal UL, UR: up left/right diagonal, left and right
THREAD_RANGE = ["DL", "DR", "UL", "UR", "R", "L"]

class Queen:
    def __init__(self, position, current, threats):
        self.old_position = position
        self.current = current
        self.threats = threats

queen_moves = 0

def search_neighbor_threats(board, position, orientation):
    x, y = position
    
    # Start checking from the next cell in the given direction
    if orientation == "DL":
        x, y = x - 1, y + 1
    elif orientation == "DR":
        x, y = x + 1, y + 1
    elif orientation == "UL":
        x, y = x - 1, y - 1
    elif orientation == "UR":
        x, y = x + 1, y - 1
    elif orientation == "R":
        x, y = x + 1, y
    elif orientation == "L":
        x, y = x - 1, y
    
    max_size = board.shape[0]
    threats = 0
    while 0 <= x < max_size and 0 <= y < max_size :
            if board[x][y] == 1:
                threats += 1
                logger.debug(f"Found threat: {x},{y}")
                break
            else:
                if orientation == "DL":
                    x, y = (x - 1, y + 1)
                elif orientation == "DR":
                    x, y = (x + 1, y + 1)
                elif orientation == "UL":
                    x, y = (x - 1, y - 1)
                elif orientation == "UR":
                    x, y = (x + 1, y - 1)
                elif orientation == "R":
                    x, y = (x + 1, y)
                elif orientation == "L":
                    x, y = (x - 1, y)
    return threats

def calculate_threats(queen, board, size):
    """Calculate the threats in the neighbors positions"""
    logger.debug("$$ Calculate threats In $$")
    next_x, next_y = queen.current[0], queen.current[1]
    logger.debug(f"Next x,y:{next_x},{next_y}")
    #check if should go up or down
    if (queen.current[1]-1) < 0:
        logger.debug("Going down")
        next_y = queen.current[1] + 1
        logger.debug(f"Looking down on the position {next_x},{next_y}")
    elif (queen.current[1]+1) > size-1:
        logger.debug("Going up")
        next_y = queen.current[1] - 1
        logger.debug(f"Looking up on the position {next_x},{next_y}")
    else:
        logger.debug("Random choice")
        next_y = queen.current[1] + rd.choice([-1,1])
        logger.debug(f"Looking random on the position {next_x},{next_y}")
    
    next_position = (next_x, next_y)
    threats = 0
    for orientation in THREAD_RANGE:
        logger.debug(f"Neighbor Threats: {threats}, Current Threats: {queen.threats} ")
        threats += search_neighbor_threats(board, next_position, orientation)
    logger.debug("$$ Calculate threats Out $$")
    return (next_position, threats)

def init_calculate_threats(board, queen):
    position = queen.current
    threats = 0
    for orientation in THREAD_RANGE:
        threats += search_neighbor_threats(board, position, orientation)
    return threats

def hill_climb(queen, board, maximize, reps):
    """Hill Climb algorithm the also implements all the variants"""
    global queen_moves
    for i in range(reps):
        neighbor = calculate_threats(queen, board, board.shape[0]) #return tuple with the threats and position
        logger.debug(f"neighbor {neighbor[0]}, {neighbor[1]}")
        if(maximize):
            if(neighbor[1] <= queen.threats):
                return queen.current, queen.threats
        else:
            logger.debug(f"checking neighbor threats: {neighbor[1]} vs current threats {queen.threats}")
            if(neighbor[1] >= queen.threats):
                logger.debug("threats not better than the neighbors")
                return queen.current, queen.threats
        logger.debug("Neighbors threats better")            
        queen.old_position = queen.current
        queen.current = neighbor[0]
        queen.threats = neighbor[1]
        board[neighbor[0][0],neighbor[0][1]]= 1
        board[queen.old_position[0],queen.old_position[1]] = 0
        queen_moves +=1
        logger.debug(f"New Move For Queen in old position: {queen.old_position}")
        #print_board(board)
        logger.debug(f"queen new position {neighbor[0]} old position {queen.old_position}")

def hill_climb_lateral_steps(queen, board, maximize, reps, lateral_step_limit):
    """Hill Climb algorithm the also implements all the variants"""
    global queen_moves
    lateral_steps = 0
    for i in range(reps):
        neighbor = calculate_threats(queen, board, board.shape[0]) #return tuple with the threats and position
        logger.debug(f"neighbor {neighbor[0]}, {neighbor[1]}")
        
        if maximize:
            improvement = neighbor[1] > queen.threats
        else:
            improvement = neighbor[1] < queen.threats
        
        if improvement or (neighbor[1] == queen.threats and lateral_steps < lateral_step_limit):
            if(neighbor[1] == queen.threats):
                lateral_steps += 1   
            
            logger.debug("Neighbors threats better")            
            queen.old_position = queen.current
            queen.current = neighbor[0]
            queen.threats = neighbor[1]
            queen_moves +=1
            board[neighbor[0][0],neighbor[0][1]]= 1
            board[queen.old_position[0],queen.old_position[1]] = 0
            logger.debug(f"New Move For Queen in old position: {queen.old_position}")
            #print_board(board)
            logger.debug(f"queen new position {neighbor[0]} old position {queen.old_position}")
        else:
            return queen.current, queen.threats 
    return queen.current, queen.threats

def init_board_and_queens(random_assigne=False, size=4):
    board = np.zeros((size, size), dtype=int)
    queens = []
    
    #init the board
    for i in range(size):
        if random_assigne:
            y = rd.randint(0, size-1) #random initiation
        else:
            y = size - 1 #all the queens at the bottom of the chess board
        board[i, y] = 1
        queens.append(Queen((i, y), (i, y), 0))

    for j in range(size):
        queens[j].threats = init_calculate_threats(board, queens[j])
        logger.debug(f"Init threats queen{j}: {queens[j].threats}")

    return board, queens

def print_board(board, queens=None):
    logger.info("---------")
    for w in range(board.shape[0]):
        logger.info(f"|{board[0,w]}|{board[1,w]}|{board[2,w]}|{board[3,w]}|")
    logger.info("---------")
    if(queens != None):
        logger.info(f"Queen1:{queens[0].current} Queen2:{queens[1].current} Queen3:{queens[2].current} Queen4:{queens[3].current}")
    
if __name__=="__main__":
    
    found_the_solution = 0
    
    for i in range(100):
        logger.debug(f"[Try:{i}]###########")
        board, queens = init_board_and_queens(True)
        #print_board(board, queens)
        
        queen_moves = 0
        old_board = board
        
        for j in range(len(queens)):
            queens.sort(key=lambda queen: queen.threats, reverse=True)
            
            #state = hill_climb(queens[j], board, False, 4)
            state = hill_climb_lateral_steps(queens[j], board, False, 4, 2)
            
            current_queen = queens[j]
            if(current_queen.old_position != state[0]):
                current_queen.current, current_queen.threats = state
                board[current_queen.current[0],current_queen.current[1]]= 1
                board[current_queen.old_position[0],current_queen.old_position[1]] = 0
                current_queen.old_position = state
                queens[j] = current_queen

        total_threats = queens[0].threats+queens[1].threats+queens[2].threats+queens[3].threats
        logger.debug(f"[Try:{i}] Total threats: {total_threats}")
        if total_threats == 0:
            logger.info("###########################################")
            logger.info(f"Moves: {queen_moves}")
            logger.info("____Start board____")
            print_board(old_board)
            logger.info("____End board____")
            print_board(board)
            found_the_solution += 1
            
    logger.info(f"Success rate: {(found_the_solution/100)*100}%")  