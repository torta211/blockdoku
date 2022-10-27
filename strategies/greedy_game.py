import numpy as np

from game import Game, get_to_clear_of_state


class GreedyGame(Game):

    def play_pieces(self):
        def get_max_score_of_piece(piece):
            piece_height, piece_width = piece.shape[0], piece.shape[1]
            piece_score = np.sum(piece)
            max_score = 0
            max_place = [-1, -1]
            for row in range(9 - piece_height + 1):
                for col in range(9 - piece_width + 1):
                    if np.max(self.field[row: row + piece_height, col: col + piece_width] + piece) == 1:
                        field_with_placement = self.field.copy()
                        field_with_placement[row: row + piece_height, col: col + piece_width] += piece
                        to_clear, combo = get_to_clear_of_state(field_with_placement)
                        score_here = np.sum(to_clear) * (self.streak_cnt + 1) * combo + piece_score
                        if score_here > max_score:
                            max_score = score_here
                            max_place = [row, col]
            return max_place[0], max_place[1], max_score
        fail = False
        success = False
        while not fail and not success:
            could_place_one = False
            places_start_i = [0, 0, 0]
            places_start_j = [0, 0, 0]
            scores = [0, 0, 0]
            max_piece_index = 1
            for i in range(3):
                if self.current_pieces[i] is None:
                    continue
                start_i, start_j, score = get_max_score_of_piece(self.current_pieces[i])
                if start_i + start_j >= 0:
                    could_place_one = True
                    places_start_i[i] = start_i
                    places_start_j[i] = start_j
                    scores[i] = score
                    if score >= scores[max_piece_index]:
                        max_piece_index = i
            if not could_place_one:
                if all(piece is None for piece in self.current_pieces):
                    success = True
                else:
                    fail = True
            else:
                self.do_place(places_start_i[max_piece_index], places_start_j[max_piece_index], max_piece_index)
        return success


if __name__ == '__main__':
    game = GreedyGame(visu=True, verbose=True, wait=0)
    game_over = False
    while not game_over:
        game.get_new_pieces()
        game_over = not game.play_pieces()
    print(f"SCORE = {game.score}")