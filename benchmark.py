from strategies import instantiate_game_by_name


def benckmark_game(game_name, num_games=1000):
    scores = []
    max_so_far = 0
    min_so_far = float("inf")
    for i in range(num_games):
        game = instantiate_game_by_name(game_name)
        game_over = False
        while not game_over:
            game.get_new_pieces()
            game_over = not game.play_pieces()
        scores.append(game.score)
        if game.score < min_so_far:
            print(f"{i}: new min score = {game.score} (avg so far = {sum(scores) / len(scores)})")
            min_so_far = game.score
        if game.score > max_so_far:
            print(f"{i}: new max score = {game.score} (avg so far = {sum(scores) / len(scores)})")
            max_so_far = game.score
    print(f"==========================================================")
    print(f"{game_name} RESULTS: min: {min_so_far}, max: {max_so_far}, avg: {sum(scores) / len(scores)}")
    print(f"==========================================================")


if __name__ == "__main__":
    benckmark_game("NaiveGame")
    benckmark_game("GreedyGame")