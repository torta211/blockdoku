import numpy as np

from game import Game, get_to_clear_of_state


class ExtremeGreedyGame(Game):

    def play_pieces(self):
        piece_height_0, piece_width_0 = self.current_pieces[0].shape[0], self.current_pieces[0].shape[1]
        piece_height_1, piece_width_1 = self.current_pieces[1].shape[0], self.current_pieces[1].shape[1]
        piece_height_2, piece_width_2 = self.current_pieces[2].shape[0], self.current_pieces[2].shape[1]
        piece_score_0 = np.sum(self.current_pieces[0])
        piece_score_1 = np.sum(self.current_pieces[1])
        piece_score_2 = np.sum(self.current_pieces[2])

        max_so_far = 0
        max_place = None

        for r0 in range(9 - piece_height_0 + 1):
            for c0 in range(9 - piece_width_0 + 1):
                field_after_first = self.field.copy()
                field_after_first[r0: r0 + piece_height_0, c0: c0 + piece_width_0] += self.current_pieces[0]
                if np.max(field_after_first[r0: r0 + piece_height_0, c0: c0 + piece_width_0]) > 1:
                    continue
                to_clear, combo = get_to_clear_of_state(field_after_first)
                field_after_first -= to_clear
                score_after_first = np.sum(to_clear) * (self.streak_cnt + 1) * combo + piece_score_0
                if combo > 0:
                    streak_after_first = self.streak_cnt + 1
                else:
                    streak_after_first = 0

                for r1 in range(9 - piece_height_1 + 1):
                    for c1 in range(9 - piece_width_1 + 1):
                        field_after_second = field_after_first.copy()
                        field_after_second[r1: r1 + piece_height_1, c1: c1 + piece_width_1] += self.current_pieces[1]
                        if np.max(field_after_second[r1: r1 + piece_height_1, c1: c1 + piece_width_1]) > 1:
                            continue
                        to_clear, combo = get_to_clear_of_state(field_after_second)
                        field_after_second -= to_clear
                        score_after_second = score_after_first + np.sum(to_clear) * (streak_after_first + 1) * combo + piece_score_1
                        if combo > 0:
                            streak_after_second = streak_after_first + 1
                        else:
                            streak_after_second = 0

                        for r2 in range(9 - piece_height_2 + 1):
                            for c2 in range(9 - piece_width_2 + 1):
                                field_after_third = field_after_second.copy()
                                field_after_third[r2: r2 + piece_height_2, c2: c2 + piece_width_2] += self.current_pieces[2]
                                if np.max(field_after_third[r2: r2 + piece_height_2, c2: c2 + piece_width_2]) > 1:
                                    continue
                                to_clear, combo = get_to_clear_of_state(field_after_third)
                                score_after_third = score_after_second + np.sum(to_clear) * (streak_after_second + 1) * combo + piece_score_2
                                if score_after_third > max_so_far:
                                    max_so_far = score_after_third
                                    max_place = (r0, c0, r1, c1, r2, c2)

        success = max_so_far > 0
        if success:
            self.do_place(max_place[0], max_place[1], 0)
            self.do_place(max_place[2], max_place[3], 1)
            self.do_place(max_place[4], max_place[5], 2)
        return success


class FirstOneShouldStepException(Exception):
    pass


class SecondOneShouldStepException(Exception):
    pass


if __name__ == '__main__':
    game = ExtremeGreedyGame(visu=True, verbose=True, wait=750)
    game_over = False
    while not game_over:
        game.get_new_pieces()
        game_over = not game.play_pieces()
    print(f"SCORE = {game.score}")