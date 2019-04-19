#python code for minmax of tictactoe

import numpy as np
# 0 is empty, 1 is X and 2 is O

def print_board(board):
    for i in range(1,10):
        print(board[i], end='')
        if (i%3 == 0):
            print()

def o_move(num, board):
    board[num] = 2

def x_move(num, board):
    board[num] = 1

def isFull(board):
    for ele in board:
        if ele == 0:
            return False
    return True

def hasWon(num, board):
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
    if (isFull(board) or hasWon(1, board) or hasWon(2, board)):
        print_board(board)
        return True
    return False

# X is positive and O is negative
def score(board):
    score_count = 0
    #row 1
    score_count += check_points(board, [1,2,3])
    #row 2
    score_count += check_points(board, [4,5,6])
    #row3
    score_count += check_points(board, [7,8,9])
    #col1
    score_count += check_points(board, [1,4,7])
    #col2
    score_count += check_points(board, [2,5,8])
    #col3
    score_count += check_points(board, [3,6,9])
    #diagonal top left to bottom right
    score_count += check_points(board, [1,5,9])
    #diagonal 2
    score_count += check_points(board, [3,5,7])
    return score_count

# assigns heuristic based on line
# what if there is 2 X's or O's in one line, still assign 1 or -1 ??
# what if the line is exclusively X's or O's (win conidtion) still 1 or -1??
def check_points(board, int_arr):
    num_x = 0
    num_o = 0
    for i in int_arr:
        if board[i] == 1:
            num_x += 1
        elif board[i] == 2:
            num_o += 1
    if (num_x > 0 and num_o == 0):
        return 1
    if (num_o > 0 and num_x == 0):
        return -1
    return 0

if __name__ == "__main__":
    board = np.zeros((10), dtype="int8")
    board[0] = 3
    while(not isEnd(board)):
        x_move(int(input("X's move\n")), board)
        if (isEnd(board)):
            break
        o_move(int(input("O's move\n")), board)
