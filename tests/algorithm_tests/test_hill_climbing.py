from src.utils.generator import Generator
from src.algorithm.solver import SokobanAlgorithm
from tests.utils.move_cache import Cache

import time

def test(game_set, game_level):
    try:
        cache = Cache()
        solver = SokobanAlgorithm()
        generator = Generator(game_set, game_level)

        stime = time.time()
        _, moves = solver.hill_climbing(generator.gen_state())
        etime = time.time() - stime

        if not moves:
            raise Exception("no solution found")

        print(f"{game_set}, {game_level}, time: {etime:.4f}")

        cache.save_move(game_set, game_level, "hill_climbing", moves)

    except Exception as e:
        print(f"error in {game_set}, {game_level}: {e}")

def test_all_levels():
    game_sets = ["miniCosmos", "microCosmos", "naboCosmos", "picoCosmos"]
    game_levels = [f"level_{i:02d}" for i in range(1, 41)]

    for game_set in game_sets:
        for i, game_level in enumerate(game_levels):
            if game_set == "picoCosmos" and i >= 20:
                break
            test(game_set, game_level)

test("naboCosmos", "level_14")