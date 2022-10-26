import numpy as np

from pieces import create_random_piece, create_field
from visu import Visualizer


class Game:
    def __init__(self, visu=None, verbose=True, wait=500):
        self.field = create_field()
        self.streak_cnt = 0
        self.score = 0
        self.current_pieces = [None, None, None]
        self.verbose = verbose
        self.visu = visu
        self.wait = wait

    def update_visu(self, wait=None):
        if self.visu is not None:
            self.visu.show_state(self.field, self.current_pieces, wait if wait else self.wait)

    def get_new_pieces(self):
        self.current_pieces = [create_random_piece(),
                               create_random_piece(),
                               create_random_piece()]
        self.update_visu()

    def do_place(self, start_i, start_j, placed_piece_index):
        piece_height = self.current_pieces[placed_piece_index].shape[0]
        piece_width = self.current_pieces[placed_piece_index].shape[1]
        piece_score = np.sum(self.current_pieces[placed_piece_index])
        self.current_pieces[placed_piece_index] *= -1
        game.field[start_i: start_i + piece_height, start_j: start_j + piece_width] += self.current_pieces[placed_piece_index]
        self.update_visu()
        game.field[start_i: start_i + piece_height, start_j: start_j + piece_width] -= self.current_pieces[placed_piece_index] * 2
        if self.verbose:
            print(f"placed piece {placed_piece_index} (+ {piece_score})")
        self.score += piece_score
        self.current_pieces[placed_piece_index] = None
        rows_to_clear = []
        cols_to_clear = []
        squares_to_clear = []
        to_clear = create_field()
        for row in range(9):
            if np.sum(self.field[row, :]) == 9:
                rows_to_clear.append(row)
                to_clear[row, :] = 1
        for col in range(9):
            if np.sum(self.field[:, col]) == 9:
                cols_to_clear.append(col)
                to_clear[:, col] = 1
        for i in range(3):
            for j in range(3):
                if np.sum(self.field[3 * i: 3 * i + 3, 3 * j: 3 * j + 3]) == 9:
                    squares_to_clear.append((i, j))
                    to_clear[3 * i: 3 * i + 3, 3 * j: 3 * j + 3] = 1
        combo = len(rows_to_clear) + len(cols_to_clear) + len(squares_to_clear)
        score = np.sum(to_clear)
        self.update_visu()
        if combo > 0:
            self.streak_cnt += 1
            self.score += self.streak_cnt * combo * score
            self.field -= 2 * to_clear
            self.update_visu()
            self.field += to_clear
            self.update_visu()
            if self.verbose:
                print(f"Combo x{combo}, Streak x{self.streak_cnt}, +{self.streak_cnt * combo * score}")
        else:
            self.streak_cnt = 0

    def play_pieces_naive(self):
        def place_one(piece):
            piece_height, piece_width = piece.shape[0], piece.shape[1]
            for row in range(9 - piece_height + 1):
                for col in range(9 - piece_width + 1):
                    if np.max(self.field[row: row + piece_height, col: col + piece_width] + piece) == 1:
                        return row, col
            return -1, -1
        fail = False
        success = False
        while not fail and not success:
            could_place_one = False
            for i in range(3):
                if self.current_pieces[i] is None:
                    continue
                start_i, start_j = place_one(self.current_pieces[i])
                if start_i + start_j >= 0:
                    self.do_place(start_i, start_j, i)
                    could_place_one = True
            if not could_place_one:
                if all(piece is None for piece in self.current_pieces):
                    success = True
                else:
                    fail = True
        return success


if __name__ == '__main__':
    game = Game(visu=Visualizer(), verbose=False)
    game_over = False
    while not game_over:
        game.get_new_pieces()
        game_over = not game.play_pieces_naive()
    print(f"SCORE = {game.score}")





