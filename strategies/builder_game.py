import numpy as np

from game import Game, get_to_clear_of_state


def get_border_length(field):
    horizontal_borders = (field[:8, :] + field[1:, :]) == 1
    vertical_borders = (field[:, :8] + field[:, 1:]) == 1
    return np.sum(horizontal_borders) + np.sum(vertical_borders)


class BuilderGame(Game):
    def play_pieces(self):
        def get_min_border_score_of_piece(piece):
            piece_height, piece_width = piece.shape[0], piece.shape[1]
            min_border = float("inf")
            min_place = [-1, -1]
            for row in range(9 - piece_height + 1):
                for col in range(9 - piece_width + 1):
                    if np.max(self.field[row: row + piece_height, col: col + piece_width] + piece) == 1:
                        field_with_placement = self.field.copy()
                        field_with_placement[row: row + piece_height, col: col + piece_width] += piece
                        border_here = get_border_length(field_with_placement)
                        if border_here < min_border:
                            min_border = border_here
                            min_place = [row, col]
            return min_place[0], min_place[1], min_border
        fail = False
        success = False
        while not fail and not success:
            could_place_one = False
            places_start_i = [0, 0, 0]
            places_start_j = [0, 0, 0]
            border_scores = [float("inf"), float("inf"), float("inf")]
            min_piece_index = 0
            for i in range(3):
                if self.current_pieces[i] is None:
                    continue
                start_i, start_j, score = get_min_border_score_of_piece(self.current_pieces[i])
                if start_i + start_j >= 0:
                    could_place_one = True
                    places_start_i[i] = start_i
                    places_start_j[i] = start_j
                    border_scores[i] = score
                    if score <= border_scores[min_piece_index]:
                        min_piece_index = i
            if not could_place_one:
                if all(piece is None for piece in self.current_pieces):
                    success = True
                else:
                    fail = True
            else:
                self.do_place(places_start_i[min_piece_index], places_start_j[min_piece_index], min_piece_index)
        return success


if __name__ == '__main__':
    game = BuilderGame(visu=True, verbose=True, wait=750)
    game_over = False
    while not game_over:
        game.get_new_pieces()
        game_over = not game.play_pieces()
    print(f"SCORE = {game.score}")