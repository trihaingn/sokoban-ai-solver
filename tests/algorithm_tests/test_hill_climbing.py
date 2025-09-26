from src.utils.generator import Generator
from src.algorithm.solver import SokobanAlgorithm
from tests.utils.move_cache import Cache

import json
import time

with open("src/utils/levels/game.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cache = Cache()
solver = SokobanAlgorithm()

for game_set in data:
    print(f"testing set: {game_set}:")
    gset = data[game_set]
    for game_level in gset:
        level = gset[game_level]
        print(f"test {game_level}:")

        state = Generator(game_set, game_level).gen_state()

        stime = time.time()
        _, moves = solver.hill_climbing(state)
        etime = time.time() - stime

        print(f"moves: {len(moves)}, time: {etime:.4f}")

        cache.save_move(game_set, game_level, "hill_climbing", moves)


