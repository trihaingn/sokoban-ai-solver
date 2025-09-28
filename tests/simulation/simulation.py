from src.utils.generator import Generator
from src.algorithm.solver import SokobanAlgorithm
from tests.utils.move_cache import Cache

generator = Generator("microCosmos", "level_19")
game = generator.gen_game()
game_set, game_level = generator.get_info()
moves = Cache().load_move(game_set, game_level)

if not moves:
    print("No cached moves found, generating new moves...")
    state = generator.gen_state()
    _, moves = SokobanAlgorithm().hybrid_heuristic(state)

game.rendering(moves)
