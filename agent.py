#!/usr/bin/python3
# Sample starter bot by Zac Partrdige
# 06/04/19

# Written by Justin Lee (Dae Ro), z5060887

import socket
import sys
import numpy as np

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
curr = 0 # this is the current board to play in

'''
My section
'''
INF = 100000
DEPTH = 1

PLAYER_X = 1
PLAYER_O = 2

# global function that determines whether start(x) or start(o)
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
        self.fullBoard = currState
        self.move = move
        self.flag = flag
        self.score = 0

    # score only needed for leaf nodes and initial alpha and beta nodes
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
        for j in range(1,10):
            for i in int_arr:
                if self.boards[j][i] == PLAYER:
                    num_player += 1
                elif self.boards[j][i] == OPPONENT:
                    num_oppo += 1
            if (num_player > 0 and num_oppo == 0):
                if (num_player == 3) :
                    ret += 1000
                else :
                    ret += num_player * 2
            elif (num_oppo > 0 and num_player == 0):
                if (num_oppo == 3) :
                    ret -= 1000
                else :
                    ret -= num_oppo * 2
        return ret


    # finds the children of the current board state
    # one is the Ai's turn
    def getChildren(self, num):
        boardsChildren = []
        for i in range(1,10):
            if (self.boards[i] == 0):
                childBoards = np.copy(self.boards)
                childBoards[i] = num
                child = MinMaxNode(self, childBoards, i, 0)
                boardsChildren.append(child)
        return boardsChildren

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
        if depth == 0 or isEnd(self.fullBoard[self.prevNode.move]): # what if the self.prevNode.move == None when depth is set to 1
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

def get_next_best_move(boards):
    check_players_set() # make sure the players are set
    m = MinMaxNode(None, boards, 0, 0)
    return m.find_minmax_move()


# checks for one sub board
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
# change later so that we only check hasWon for the player that made the move
def isEnd(board):
    if (isFull(board) or hasWon(board, 1) or hasWon(board, 2)):
        return True
    return False

# CHECK THAT THE PLAYER AND OPPONENT HAS BEEN SET
# Doesnt need to be set, just extra precaution
def check_players_set():
    global PLAYER
    global OPPONENT
    if PLAYER == 1 and OPPONENT == 2:
        return True
    elif PLAYER == 2 and OPPONENT == 1:
        return True
    sys.exit("player(X) and player(O) not set")
    return False

# set the global variable of the player and the opponent for the AI.
def set_player(c):
    global PLAYER
    global OPPONENT
    if (c == "x") :
        PLAYER = 1
    elif (c == "o"):
        PLAYER = 2
    else:
        sys.exit("unknown string to set player")
    if PLAYER == 1 :
        OPPONENT = 2
    else :
        OPPONENT = 1
    check_players_set()
'''
END of mySection
'''

# print a row
# This is just ported from game.c
def print_board_row(board, a, b, c, i, j, k):
    # The marking script doesn't seem to like this either, so just take it out to submit
    print("", board[a][i], board[a][j], board[a][k], end = " | ")
    print(board[b][i], board[b][j], board[b][k], end = " | ")
    print(board[c][i], board[c][j], board[c][k])

# Print the entire board
# This is just ported from game.c
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()

# choose a move to play
def play():
    global boards
    # print_board(boards)

    # just play a random move for now
    n = np.random.randint(1,9)
    while boards[curr][n] != 0:
        n = np.random.randint(1,9)

    # print("playing", n)
    place(curr, n, 1)
    return n

# place a move in the global boards
def place(board, num, player):
    global curr
    global boards
    curr = num
    boards[board][num] = player
    print_board(board)

# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command == "second_move":
        place(int(args[0]), int(args[1]), 2)
        return play()
    elif command == "third_move":
        # place the move that was generated for us
        place(int(args[0]), int(args[1]), 1)
        # place their last move
        place(curr, int(args[2]), 2)
        return play()
    elif command == "next_move":
        place(curr, int(args[0]), 2)
        return play()
    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    elif command == "start":
        set_player(args[0])
    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        print(text)
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                print((str(response) + "\n"))
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()