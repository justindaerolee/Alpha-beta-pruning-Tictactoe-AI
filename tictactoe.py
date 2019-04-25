#python code for minmax of tictactoe

import numpy as np
# 0 is empty, 1 is X and 2 is O

INF = 100000
DEPTH = 4

# MinMaxNode class definition
class MinMaxNode:
    def __init__(self, prevNode, currState, move, score):
        self.prevNode = prevNode
        self.board = currState
        self.move = move
        if currState is None:
            self.score = score
        else:
            self.score = self.score()

    def score(self):
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
    # x is negative because it is our turn and O is the Ai's turn
    def check_points(self, int_arr):
        num_x = 0
        num_o = 0
        ret = 0
        for i in int_arr:
            if self.board[i] == 1:
                num_x += 1
            elif self.board[i] == 2:
                num_o += 1

        if (num_x > 0 and num_o == 0):
            if (num_x == 3) :
                ret = - 1000
            else :
                ret = - num_x * 2
            return ret
        if (num_o > 0 and num_x == 0):
            if (num_o == 3) :
                ret = 1000
            else :
                ret = num_o * 2
            return ret
        return 0


    # finds the children of the board, helper function for funct alphabeta
    # one is the Ai's turn
    def getChildren(self, num):
        if (num == 1):
            return self.getChildrenHelper(2)
        else:
            return self.getChildrenHelper(1)
        return None

    # num specifies whether it is X's or O's move. num =1 for X, num=2 for O
    # return the children as MinMaxNode object
    def getChildrenHelper(self, num):
        boardChildren = []
        for i in range(1,10):
            if (self.board[i] == 0):
                childBoard = np.copy(self.board)
                childBoard[i] = num
                child = MinMaxNode(self, childBoard, i, 0)
                boardChildren.append(child)
        return boardChildren

    # X is positive and O is negative
    def print_board(self):
        print()
        for i in range(1,10):
            print(self.board[i], end='')
            if (i%3 == 0):
                print()

    def o_move(self, move):
        self.board[move] = 2

    def x_move(self, move):
        self.board[move] = 1

    def isFull(self):
        for ele in self.board:
            if ele == 0:
                return False
        return True

    def hasWon(self, num):
        return (
            (self.board[1] == num and self.board[2] == num and self.board[3] == num) or
            (self.board[4] == num and self.board[5] == num and self.board[6] == num) or
            (self.board[7] == num and self.board[8] == num and self.board[9] == num) or
            (self.board[1] == num and self.board[4] == num and self.board[7] == num) or
            (self.board[2] == num and self.board[5] == num and self.board[8] == num) or
            (self.board[3] == num and self.board[6] == num and self.board[9] == num) or
            (self.board[1] == num and self.board[5] == num and self.board[9] == num) or
            (self.board[3] == num and self.board[5] == num and self.board[7] == num)
            )

    def isEnd(self):
        if (self.isFull() or self.hasWon(1) or self.hasWon(2)):
            return True
        return False
### End of class Definition




''' sudo code from AI lecture
function alphabeta( node, depth, α, β )
    if node is terminal or depth = 0 { return heuristic value of node }
    if we are to play at node
        foreach child of node
            let α = max( α, alphabeta( child, depth-1, α, β ))
            if α ≥ β { return α }
        return α
    else // opponent is to play at node
        foreach child of node
            let β = min( β, alphabeta( child, depth-1, α, β ))
            if β ≤ α { return β }
        return β
'''
def minmax(node):
    global INF
    global DEPTH
    alpha = MinMaxNode(None, None, 0, -INF)
    beta = MinMaxNode(None, None, 0, INF)
    return alphabeta(node, DEPTH, alpha, beta, 1)

# alpha beta pruning, num ==1 for our turn num == -1 for the others turn
def alphabeta(node, depth, alpha, beta, num):
    if depth == 0 or node.isEnd():
        #print(node.score)
        return node
    if num == 1:
        for child in node.getChildren(num):
            childNode = alphabeta(child, depth-1, alpha, beta, -1)
            if childNode.score > alpha.score :
                alpha = childNode
            if alpha.score >= beta.score :
                break
        return alpha
    else:
        for child in node.getChildren(num):
            childNode = alphabeta(child, depth-1, alpha, beta, 1)
            if (childNode.score < beta.score) :
                beta = childNode
            if alpha.score >= beta.score :
                break
        return beta

def find_first_move(node):
    tmp = node
    while node.prevNode is not None:
        tmp = node
        node = tmp.prevNode
    return tmp.move

def play():
    board = np.zeros((10), dtype="int8")
    board[0] = 3
    node = MinMaxNode(None, board, 0, 0)
    while(not node.isEnd()):
        node.x_move(int(input("X's move\n")))
        node.print_board()
        if (node.isEnd()):
            break
        a = minmax(node)
        node.o_move(int(find_first_move(a)))
        node.print_board()
def test():
    board = np.zeros((10), dtype="int8")
    board[0] = 3
    node = MinMaxNode(None, board, 0, 0)
    board[1] = 1
    node = MinMaxNode(None, board, 0, 0)
    print(node.score)

if __name__ == "__main__":
    play()
