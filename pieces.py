import random
import numpy as np

PIECES = [
    # ONE BLOCK
    np.array([[1]]),
    # TWO BLOCKS
    np.array([[1, 1]]),
    np.array([[1],
              [1]]),
    # THREE BLOCKS
    np.array([[1, 1, 1]]),
    np.array([[1],
              [1],
              [1]]),
    np.array([[1, 1],
              [1, 0]]),
    np.array([[1, 1],
              [0, 1]]),
    np.array([[1, 0],
              [1, 1]]),
    np.array([[0, 1],
              [1, 1]]),
    # FOUR BLOCKS
    np.array([[1, 1, 1, 1]]),
    np.array([[1],
              [1],
              [1],
              [1]]),
    np.array([[1, 1],
              [1, 1]]),
    #       standing L
    np.array([[1, 1],
              [1, 0],
              [1, 0]]),
    np.array([[1, 1],
              [0, 1],
              [0, 1]]),
    np.array([[1, 0],
              [1, 0],
              [1, 1]]),
    np.array([[0, 1],
              [0, 1],
              [1, 1]]),
    #       laying L
    np.array([[1, 1, 1],
              [0, 0, 1]]),
    np.array([[0, 0, 1],
              [1, 1, 1]]),
    np.array([[1, 1, 1],
              [1, 0, 0]]),
    np.array([[1, 0, 0],
              [1, 1, 1]]),
    #       standing Z
    np.array([[0, 1],
              [1, 1],
              [1, 0]]),
    np.array([[1, 0],
              [1, 1],
              [0, 1]]),
    #       laying Z
    np.array([[0, 1, 1],
              [1, 1, 0]]),
    np.array([[1, 1, 0],
              [0, 1, 1]]),
    #       standing halfplus
    np.array([[1, 0],
              [1, 1],
              [1, 0]]),
    np.array([[0, 1],
              [1, 1],
              [0, 1]]),
    #       laying halfplus
    np.array([[1, 1, 1],
              [0, 1, 0]]),
    np.array([[0, 1, 0],
              [1, 1, 1]]),
    # FIVE BLOCKS
    np.array([[1, 1, 1, 1, 1]]),
    np.array([[1],
              [1],
              [1],
              [1],
              [1]]),
    np.array([[1, 1, 1],
              [1, 0, 0],
              [1, 0, 0]]),
    np.array([[1, 1, 1],
              [0, 0, 1],
              [0, 0, 1]]),
    np.array([[0, 0, 1],
              [0, 0, 1],
              [1, 1, 1]]),
    np.array([[1, 0, 0],
              [1, 0, 0],
              [1, 1, 1]]),
    np.array([[1, 0, 1],
              [1, 1, 1]]),
    np.array([[1, 1],
              [0, 1],
              [1, 1]]),
    np.array([[1, 1, 1],
              [1, 0, 1]]),
    np.array([[1, 1],
              [1, 0],
              [1, 1]]),
    np.array([[1, 1, 1],
              [0, 1, 0],
              [0, 1, 0]]),
    np.array([[1, 0, 0],
              [1, 1, 1],
              [1, 0, 0]]),
    np.array([[0, 1, 0],
              [0, 1, 0],
              [1, 1, 1]]),
    np.array([[0, 0, 1],
              [1, 1, 1],
              [0, 0, 1]])
]


def create_random_piece():
    return PIECES[random.randint(0, len(PIECES) - 1)]


def create_field():
    return np.array([[0 for _ in range(9)] for _ in range(9)])