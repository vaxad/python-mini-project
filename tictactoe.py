"""
Tic Tac Toe Player
"""
import copy
# import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    number_of_x = 0
    number_of_o = 0

    for row in range(3):
        for col in range(3):
            if board[row][col] == X:
                number_of_x += 1
            elif board[row][col] == O:
                number_of_o += 1

    if number_of_x == number_of_o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    action = []

    for row in range(3):
        for col in range(3):
            if board[row][col] is EMPTY:
                action.append((row, col))

    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if board[action[0]][action[1]] is not EMPTY:
        raise ActionNotValidException()

    copy_board = copy.deepcopy(board)
    copy_board[action[0]][action[1]] = player(board)

    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # CHECKING IF X WINS THE GAME

    for row in range(3):
        count = 0
        for col in range(3):
            if board[row][col] is X:
                count += 1
        if count == 3:
            return X

    for row in range(3):
        count = 0
        for col in range(3):
            if board[col][row] is X:
                count += 1
        if count == 3:
            return X

    count = 0
    for row in range(3):
        for col in range(3):
            if col == row and board[row][col] is X:
                count += 1
    if count == 3:
        return X

    if board[1][1] is X and board[0][2] is X and board[2][0] is X:
        return X

    # CHECKING IF O WINS THE GAME

    for row in range(3):
        count = 0
        for col in range(3):
            if board[row][col] is O:
                count += 1
        if count == 3:
            return O

    for row in range(3):
        count = 0
        for col in range(3):
            if board[col][row] is O:
                count += 1
        if count == 3:
            return O

    count = 0
    for row in range(3):
        for col in range(3):
            if col == row and board[row][col] is O:
                count += 1
    if count == 3:
        return O

    if board[1][1] is O and board[0][2] is O and board[2][0] is O:
        return O


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    count = 0
    for row in board:
        for element in row:
            if element == EMPTY:
                count += 1

    if winner(board) is not EMPTY or count == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            v = -5
            ans = None
            for action in actions(board):
                new_board = result(board, action)
                if min_value(new_board) > v:
                    v = min_value(new_board)
                    ans = action

            # return max(min_value(result(board, action)) for action in actions(board))

        elif player(board) == O:
            v = 5
            ans = None
            for action in actions(board):
                new_board = result(board, action)
                if max_value(new_board) < v:
                    v = max_value(new_board)
                    ans = action
            return ans

            # return max(max_value(result(board, action)) for action in actions(board))


def min_value(board):
    """
    Returns the minimal value of a given state of the game if
    both players play optimally
    """

    v = 5

    if terminal(board):
        return utility(board)

    for action in actions(board):
        new_board = result(board, action)
        v_1 = max_value(new_board)
        v = min(v_1, v)

    return v


def max_value(board):
    """
    Returns the maximum value of a given state of the game if
    both players play optimally
    """

    v = -5

    if terminal(board):
        return utility(board)

    for action in actions(board):
        new_board = result(board, action)
        v_1 = min_value(new_board)
        v = max(v_1, v)

    return v


class ActionNotValidException(Exception):
    def __init__(self):
        print("Action is not valid for current board configuration")