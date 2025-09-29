from src.utils.generator import Generator
from src.algorithm.solver import SokobanAlgorithm
from tests.utils.move_cache import Cache
from tests.utils.timeout import timeout

import time

@timeout(120)
def test(game_set, game_level):
    try:  
        cache = Cache()
        generator = Generator(game_set, game_level)
        state = generator.gen_state()
        solver = SokobanAlgorithm(state)

        print(f"{game_set}, {game_level}")  
        stime = time.time()
        _, moves = solver.hybrid_heuristic()
        etime = time.time() - stime

        if not moves:
            raise Exception("no solution found")

        print(f"time: {etime:.4f}")

        cache.save_move(game_set, game_level, "hybrid_heuristic", moves)

    except Exception as e:
        print(f"error in {game_set}, {game_level}: {e}")

def test_all():
    game_sets = ["miniCosmos", "microCosmos", "naboCosmos", "picoCosmos"]
    game_levels = [f"level_{i:02d}" for i in range(1, 41)]

    for game_set in game_sets:
        for i, game_level in enumerate(game_levels):
            if game_set == "picoCosmos" and i >= 20:
                break
            test(game_set, game_level)

test_all()