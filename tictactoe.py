#python code for minmax of tictactoe

import numpy as np
import sys
# 0 is empty, 1 is X and 2 is O

INF = 100000
DEPTH = 1

PLAYER_X = 1
PLAYER_O = 2

# global function that determines whether PLAYER_X or PLAYER_O
PLAYER = 0
OPPONENT = 0

IS_ALPHA_FLAG = 2
IS_BETA_FLAG = 3

# MinMaxNode class definition
class MinMaxNode:
    # flag = 0 (is non-leaf), 1 (leaf), 2 (initial alpha), 3 (intial beta)
    def __init__(self, prevNode, currState, move, flag):
        global INF
        self.prevNode = prevNode
        self.board = currState
        self.move = move
        self.flag = flag
        self.score = 0

    def get_score(self):
        global INF
        ret = 0
        if (self.flag == 1) :
            ret = self.score
        elif self.flag == 2:
            ret = - INF
        elif self.flag == 3 :
            ret = INF
        else :
            sys.exit("Cannot access score of non-leaf nodes")
        return ret

    def calculate_score(self):
        self.flag = 1
        self.score = self.get_heuristic()

    # Wrapper function to calculate the heuristic score of the boards
    def get_heuristic(self):
        score_count = 0
        #row 1
        score_count += self.check_points([1,2,3])
        #row 2
        score_count += self.check_points([4,5,6])
        #row3
        score_count += self.check_points([7,8,9])
        #col1
        score_count += self.check_points([1,4,7])
        #col2
        score_count += self.check_points([2,5,8])
        #col3
        score_count += self.check_points([3,6,9])
        #diagonal top left to bottom right
        score_count += self.check_points([1,5,9])
        #diagonal 2
        score_count += self.check_points([3,5,7])
        return score_count

    # assigns heuristic based on line
    def check_points(self, int_arr):
        global PLAYER
        global OPPONENT
        num_player = 0
        num_oppo = 0
        ret = 0
        for i in int_arr:
            if self.board[i] == PLAYER:
                num_player += 1
            elif self.board[i] == OPPONENT:
                num_oppo += 1
        if (num_player > 0 and num_oppo == 0):
            if (num_player == 3) :
                ret = 1000
            else :
                ret = num_player * 2
        elif (num_oppo > 0 and num_player == 0):
            if (num_oppo == 3) :
                ret = - 1000
            else :
                ret = - num_oppo * 2
        return ret


    # finds the children of the current board state
    # one is the Ai's turn
    def getChildren(self, num):
        boardChildren = []
        for i in range(1,10):
            if (self.board[i] == 0):
                childBoard = np.copy(self.board)
                childBoard[i] = num
                child = MinMaxNode(self, childBoard, i, 0)
                boardChildren.append(child)
        return boardChildren

    # wrapper function for alpha beta pruning
    def minmax(self):
        global INF
        global DEPTH
        global IS_ALPHA_FLAG
        global IS_BETA_FLAG
        global PLAYER
        alpha = MinMaxNode(None, None, 0, IS_ALPHA_FLAG)
        beta = MinMaxNode(None, None, 0, IS_BETA_FLAG)
        return self.alphabeta(DEPTH, alpha, beta, PLAYER)

    # alpha beta pruning
    def alphabeta(self, depth, alpha, beta, num):
        global PLAYER
        global OPPONENT
        if depth == 0 or isEnd(self.board):
            self.calculate_score()
            return self
        if num == PLAYER:
            for child in self.getChildren(PLAYER):
                childNode = child.alphabeta(depth-1, alpha, beta, OPPONENT)
                if childNode.get_score() > alpha.get_score() :
                    alpha = childNode
                if alpha.get_score() >= beta.get_score() :
                    break
            return alpha
        else:
            for child in self.getChildren(OPPONENT):
                childNode = child.alphabeta(depth-1, alpha, beta, PLAYER)
                if (childNode.get_score() < beta.get_score()) :
                    beta = childNode
                if alpha.get_score() >= beta.get_score() :
                    break
            return beta

    def find_minmax_move(self):
        node = self.minmax()
        tmp = node
        while node.prevNode is not None:
            tmp = node
            node = tmp.prevNode
        return tmp.move

### End of class Definition


def get_next_best_move(board, move):
    check_players_set() # make sure the players are set
    m = MinMaxNode(None, board, move, 0)
    return m.find_minmax_move()


def print_board(board):
    print()
    for i in range(1,10):
        print(board[i], end='')
        if (i%3 == 0):
            print()

def isFull(board):
    for ele in board:
        if ele == 0:
            return False
    return True

def hasWon(board, num):
    return (
        (board[1] == num and board[2] == num and board[3] == num) or
        (board[4] == num and board[5] == num and board[6] == num) or
        (board[7] == num and board[8] == num and board[9] == num) or
        (board[1] == num and board[4] == num and board[7] == num) or
        (board[2] == num and board[5] == num and board[8] == num) or
        (board[3] == num and board[6] == num and board[9] == num) or
        (board[1] == num and board[5] == num and board[9] == num) or
        (board[3] == num and board[5] == num and board[7] == num)
        )

def isEnd(board):
    if (isFull(board) or hasWon(board, 1) or hasWon(board, 2)):
        return True
    return False


def check_players_set():
    global PLAYER
    global OPPONENT
    if PLAYER == 1 and OPPONENT == 2:
        return True
    elif PLAYER == 2 and OPPONENT == 1:
        return True
    sys.exit("player(X) and player(O) not set")
    return False

def set_player(num):
    global PLAYER
    global OPPONENT
    PLAYER = num
    if num == 1 :
        OPPONENT = 2
    else :
        OPPONENT = 1
    check_players_set()

def ai_turn(board, move):
    global PLAYER
    board[move] = PLAYER
    print_board(board)
    if (isEnd(board)):
        return False
    return True
def oppo_turn(board, move):
    global OPPONENT
    print("AI's move" + str(move))
    board[move] = OPPONENT
    print_board(board)
    if (isEnd(board)):
        return False
    return True

def play():
    global PLAYER
    board = np.zeros((10), dtype="int8")
    board[0] = 3
    set_player(int(input("select AI's turn, 1 for X, 2 for O\n")))
    flag = True
    while(flag):
        if (PLAYER == 1) :
            flag = ai_turn(board, get_next_best_move(board))
            if not flag :
                break
            flag = oppo_turn(board, int(input("Your move\n")))
        else :
            flag = oppo_turn(board, int(input("Your move\n")))
            if not flag :
                break
            flag = ai_turn(board, get_next_best_move(board))

def test():
    board = np.zeros((10), dtype="int8")
    board[0] = 3
    node = MinMaxNode(None, board, 0, 0)
    board[1] = 1
    node = MinMaxNode(None, board, 0, 0)
    print(node.get_score())

if __name__ == "__main__":
    play()
