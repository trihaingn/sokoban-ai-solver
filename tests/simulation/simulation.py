from src.utils.generator import Generator
from src.algorithm.solver import SokobanAlgorithm
from tests.utils.move_cache import Cache

game_set = "microCosmos"
game_level = "level_01"

generator = Generator(game_set, game_level)
game = generator.gen_game()
moves = Cache().load_move(game_set, game_level)

if not moves:
    state = generator.gen_state()
    _, moves = SokobanAlgorithm().hill_climbing(state)

game.rendering(moves)
