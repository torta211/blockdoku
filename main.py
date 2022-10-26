import numpy as np

from pieces import create_random_piece, create_field


class Game:
    def __init__(self, verbose=True):
        self.field = create_field()
        self.streak_cnt = 0
        self.score = 0
        self.current_pieces = [None, None, None]
        self.verbose = verbose

    def get_new_pieces(self):
        self.current_pieces = [create_random_piece(),
                               create_random_piece(),
                               create_random_piece()]

    def after_placement(self, placed_piece_index):
        piece_score = np.sum(self.current_pieces[placed_piece_index])
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
        if combo > 0:
            self.streak_cnt += 1
            self.score += self.streak_cnt * combo * score
            self.field -= to_clear
            if self.verbose:
                print(f"Combo x{combo}, Streak x{self.streak_cnt}, +{self.streak_cnt * combo * score}")
        else:
            self.streak_cnt = 0

    def play_pieces_naive(self):
        def place_one(game, piece):
            piece_width = piece.shape[1]
            piece_height = piece.shape[0]
            for row in range(9 - piece_height + 1):
                for col in range(9 - piece_width + 1):
                    if np.max(self.field[row: row + piece_height, col: col + piece_width] + piece) == 1:
                        game.field[row: row + piece_height, col: col + piece_width] += piece
                        return True
        for i in range(3):
            if place_one(self, self.current_pieces[i]):
                self.after_placement(i)
            else:
                return False
        return True


if __name__ == '__main__':
    game = Game()
    game_over = False
    while not game_over:
        game.get_new_pieces()
        game_over = not game.play_pieces_naive()
    a = 6





