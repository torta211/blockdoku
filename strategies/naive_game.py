import numpy as np

from game import Game


class NaiveGame(Game):

    def play_pieces(self):
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
    game = NaiveGame(visu=True, verbose=False)
    game_over = False
    while not game_over:
        game.get_new_pieces()
        game_over = not game.play_pieces()
    print(f"SCORE = {game.score}")