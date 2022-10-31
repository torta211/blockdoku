import numpy as np

from typing import final
from abc import abstractmethod

from pieces import create_random_piece, create_field
from visu import Visualizer


def get_to_clear_of_state(field):
    rows_to_clear = np.where(np.sum(field, axis=1) == 9)[0]
    cols_to_clear = np.where(np.sum(field, axis=0) == 9)[0]
    squares_to_clear = []
    to_clear = create_field()
    to_clear[rows_to_clear, :] = 1
    to_clear[:, cols_to_clear] = 1
    for i in range(3):
        row_start = 3 * i
        for j in range(3):
            if np.sum(field[row_start: row_start + 3, 3 * j: 3 * j + 3]) == 9:
                squares_to_clear.append((i, j))
                to_clear[row_start: row_start + 3, 3 * j: 3 * j + 3] = 1
    return to_clear, len(rows_to_clear) + len(cols_to_clear) + len(squares_to_clear)


class Game:
    def __init__(self, visu=True, verbose=True, wait=500):
        self.field = create_field()
        self.streak_cnt = 0
        self.score = 0
        self.current_pieces = [None, None, None]
        self.verbose = verbose
        self.visu = Visualizer() if visu else None
        self.wait = wait

    def __update_visu(self, wait=None):
        if self.visu is not None:
            self.visu.show_state(self.field, self.current_pieces, wait if wait else self.wait)

    @final
    def get_new_pieces(self):
        if all(piece is None for piece in self.current_pieces):
            self.current_pieces = [create_random_piece(),
                                   create_random_piece(),
                                   create_random_piece()]
            self.__update_visu()
        else:
            raise Exception("Invalid move: attempted to get new pieces before placing the previous ones!")

    @final
    def do_place(self, start_i, start_j, placed_piece_index):
        piece_height = self.current_pieces[placed_piece_index].shape[0]
        piece_width = self.current_pieces[placed_piece_index].shape[1]
        if np.max(self.field[start_i: start_i + piece_height, start_j: start_j + piece_width] +
                  self.current_pieces[placed_piece_index]) > 1:
            raise Exception("Invalid move: attempted to place a piece at an occupied location!")
        piece_score = np.sum(self.current_pieces[placed_piece_index])
        self.score += piece_score
        if self.verbose:
            print(f"{self.score} - placed piece {placed_piece_index} (+ {piece_score})")
        # negative numbers are only for visu, we basically add the piece to the field (/board) and remove it from set
        #   highlighting placed piece with negative value
        self.current_pieces[placed_piece_index] *= -1
        #   highlighting placement with negative value
        self.field[start_i: start_i + piece_height, start_j: start_j + piece_width] += self.current_pieces[placed_piece_index]
        self.__update_visu()
        #   adding piece (was multiplied by -1)
        self.field[start_i: start_i + piece_height, start_j: start_j + piece_width] -= self.current_pieces[placed_piece_index] * 2
        self.current_pieces[placed_piece_index] = None
        # calcu
        to_clear, combo = get_to_clear_of_state(self.field)
        score = np.sum(to_clear)
        self.__update_visu()
        if combo > 0:
            self.streak_cnt += 1
            self.score += self.streak_cnt * combo * score
            # highlight to_clear
            self.field -= 2 * to_clear
            self.__update_visu()
            if self.verbose:
                print(f"{self.score} - combo x{combo}, Streak x{self.streak_cnt}, +{self.streak_cnt * combo * score}")
            # remove to_clear
            self.field += to_clear
            self.__update_visu()
        else:
            self.streak_cnt = 0

    @abstractmethod
    def play_pieces(self):
        print("HOPELESS STRATEGY :( PLEASE OVERRIDE IT")
        return False


if __name__ == '__main__':
    game = Game(visu=True, verbose=False)
    game_over = False
    while not game_over:
        game.get_new_pieces()
        game_over = not game.play_pieces()
    print(f"SCORE = {game.score}")





