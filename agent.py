#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
# Sample starter bot by Zac Partrdige
# 06/04/19

# Written by Justin Lee (Dae Ro), z5060887
#            William Ye, z5061340

import socket
import sys
import numpy as np

# A board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# The boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int32")
curr = 0 # this is the current board to play in

INF = 1000000
DEPTH = 5 # Starting depth of search
MOVE = 0

PLAYER_X = 1
PLAYER_O = 2

# Global function that determines whether start(x) or start(o)
PLAYER = 0
OPPONENT = 0



# MinMaxNode class definition
class MinMaxNode:
    def __init__(self, prevNode, currState, move, scores):
        global INF
        self.prevNode = prevNode
        self.fullBoard = currState
        self.move = move
        self.scores = scores

    # Calculate the heuristic by summing all the scores of subgrids
    def getScore(self):
        ret = 0
        for x in self.scores :
            ret += x
        return ret

    # Sets the score for the initial Min Max Node
    def setScore(self):
        scoreCount = 0
        # Get score for each 3x3 on board and set it
        for j in range(1,10):
            num = self.checkGrid(j)
            # print("ASDF" + str(num))
            self.scores[j] = num

    # Calculates the heuristic for a subgrid
    def checkGrid(self, board_num):
        ret = 0
        arr = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
        for x in range(8):
            score = self.checkLine(arr[x], board_num)
            if score == 1000 or score == -1000:
                return score
            else:
                ret += score
        return ret

    # Calculates the heuristic for a single line of a subgrid
    def checkLine(self, arr, board_num):
        global PLAYER
        global OPPONENT
        num_player = 0
        num_oppo = 0

        for x in range(3):
            if self.fullBoard[board_num][arr[x]] == PLAYER:
                num_player += 1
            elif self.fullBoard[board_num][arr[x]] == OPPONENT:
                num_oppo += 1

        if num_player == 3:
            # Player wins
            return 1000
        elif num_oppo == 3:
            # Opponent wins
            return -1000
        elif (num_player == 2 and num_oppo == 0):
            # Player has big advantage
            return 10
        elif (num_player == 1 and num_oppo == 0):
            # Player has small advantage
            return 1
        elif (num_oppo == 2 and num_player == 0):
            # Opponent has big advantage
            return -10
        elif (num_oppo == 1 and num_player == 0):
            # Opponent has small advantage
            return -1
        else:
            # no advantage
            return 0


    # Finds the children of the current board state and assigns a score
    # based on iterative heuristic calculation
    def getChildren(self, targetBoard, num):
        boardsChildren = []
        for i in range(1,10):
            if (self.fullBoard[targetBoard][i] == 0):
                childBoards = np.copy(self.fullBoard)
                childBoards[targetBoard][i] = num
                tmp = MinMaxNode(self, childBoards, i, 0)
                scores2 = np.copy(self.prevNode.scores)
                scores2[targetBoard] = tmp.checkGrid(targetBoard)

                # Avoid subgrid that opponent is winning
                if scores2[i] < -10:
                    scores2[i] -= 50

                child = MinMaxNode(self, childBoards, i, scores2)
                boardsChildren.append(child)
        return boardsChildren

    # Wrapper function for alpha beta pruning
    def minmax(self):
        global INF
        global DEPTH
        global PLAYER
        alpha = MinMaxNode(None, None, 0, [-INF,0,0,0,0,0,0,0,0,0])
        beta = MinMaxNode(None, None, 0, [INF,0,0,0,0,0,0,0,0,0])
        return self.alphabeta(DEPTH, alpha, beta, PLAYER)

    # Alpha-Beta Pruning
    def alphabeta(self, depth, alpha, beta, num):
        global PLAYER
        global OPPONENT
        if depth == 0 or isEnd(self.fullBoard[self.prevNode.move]): # what if the self.prevNode.move == None when depth is set to 1
            return self
        elif num == PLAYER:
            for child in self.getChildren(self.move, PLAYER):
                childNode = child.alphabeta(depth-1, alpha, beta, OPPONENT)
                if childNode.getScore() > alpha.getScore() :
                    alpha = childNode
                if alpha.getScore() >= beta.getScore() :
                    break
            return alpha
        else:
            for child in self.getChildren(self.move, OPPONENT):
                childNode = child.alphabeta(depth-1, alpha, beta, PLAYER)
                if (childNode.getScore() < beta.getScore()) :
                    beta = childNode
                if alpha.getScore() >= beta.getScore() :
                    break
            return beta

    # Returns move based on MinMax search
    def findMinmaxMove(self):
        node = self.minmax()
        print("The score alphabeta pruning is " + str(node.getScore()))
        tmp = node
        while node.prevNode.prevNode is not None:
            tmp = node
            node = tmp.prevNode
        return tmp.move

# Gets the best move to be sent to server
def getNextBestMove(fullBoard, move):
    global curr
    checkPlayersSet() # make sure the players are set
    prev = MinMaxNode(None, None, curr, np.zeros(10, dtype="int32"))
    m = MinMaxNode(prev, fullBoard, move, np.zeros(10, dtype="int32"))
    m.setScore()
    return m.findMinmaxMove()


# Checks if the board is full
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

# Precautionary check to see if players have been set
def checkPlayersSet():
    global PLAYER
    global OPPONENT
    if PLAYER == 1 and OPPONENT == 2:
        return True
    elif PLAYER == 2 and OPPONENT == 1:
        return True
    sys.exit("player(X) and player(O) not set")
    return False

# Set the global variable of the player and the opponent for the AI.
def setPlayer(c):
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
    checkPlayersSet()

# Prints a row
# Ported from game.c
def print_board_row(board, a, b, c, i, j, k):
    # The marking script doesn't seem to like this either, so just take it out to submit
    print("", board[a][i], board[a][j], board[a][k], end = " | ")
    print(board[b][i], board[b][j], board[b][k], end = " | ")
    print(board[c][i], board[c][j], board[c][k])

# Print the entire board
# Ported from game.c
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

# Choose a move to play
def play():
    global boards
    n = np.random.randint(1,9)
    while boards[curr][n] != 0:
        n = np.random.randint(1,9)
    return n

# Place a move on the global board
def place(board, num, player):
    global curr
    global boards
    curr = num
    boards[board][num] = player

# Takes the string sent from the server and parses it for relevant information
def parse(string):
    global curr
    global PLAYER
    global OPPONENT
    global MOVE
    global DEPTH
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command == "second_move":
        place(int(args[0]), int(args[1]), OPPONENT)
        bestMove = getNextBestMove(boards, int(args[1]))
        place(curr, bestMove, PLAYER)
        MOVE += 1
        return bestMove
    elif command == "third_move":
        # Place the move that was generated for us
        place(int(args[0]), int(args[1]), PLAYER)
        # Places their last move
        place(curr, int(args[2]), OPPONENT)
        bestMove = getNextBestMove(boards, int(args[2]))
        place(curr, bestMove, PLAYER)
        MOVE += 1
        return bestMove
    elif command == "next_move":
        place(curr, int(args[0]), OPPONENT)
        bestMove = getNextBestMove(boards, int(args[0]))
        place(curr, bestMove, PLAYER)
        MOVE += 1
        # Increase depth of search by 1 every 7 moves
        if MOVE % 7 == 0:
            DEPTH += 1
        return bestMove
    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    elif command == "start":
        setPlayer(args[0])
    return 0

# Connecting to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2])

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
