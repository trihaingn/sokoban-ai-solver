from src.utils.generator import Generator
from src.algorithm.solver import SokobanAlgorithm
from tests.utils.move_cache import Cache

def simulate(game_set, game_level):
    generator = Generator(game_set, game_level)
    game = generator.gen_game()
    moves = Cache().load_move(game_set, game_level)

    if not moves:
        state = generator.gen_state()
        _, moves = SokobanAlgorithm().hybrid_heuristic(state)

    game.rendering(moves)

simulate("picoCosmos", "level_10")
