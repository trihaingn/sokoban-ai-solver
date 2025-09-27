import json
import random
from src.core.state import SokobanState
from src.core.game import SokobanGame

game_sets = ["microCosmos", "miniCosmos"]

class Generator:
    def __init__(self, game_set = None, game_level = None):
        with open("src/utils/levels/game.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        if not game_set:
            game_set = random.choice(game_sets)  
            print(f"Randomly selected game set: {game_set}")

        self.game_set = game_set

        _game_set = data.get(game_set, None)
        
        if not _game_set:
            raise Exception("Level set not found")
        else:
            if not game_level:
                def random_level():
                    num = random.randint(1, 40)
                    return f"level_{num:02d}"
                
                game_level = random_level()
                print(f"Randomly selected game level: {game_level}")

            level_str = _game_set.get(game_level, None)

            self.game_level = game_level

            if not level_str:
                raise Exception("Level not found")
            else:
                self.player = None
                self.crates = set()
                self.obstacles = set()
                self.targets = set()

                lines = level_str.splitlines()

                maxX = len(lines)
                maxY = 0

                for r, line in enumerate(lines):
                    maxY = max(maxY, len(line))
                    for c, ch in enumerate(line):
                        pos = (r,c)
                        if ch == '#':
                            self.obstacles.add(pos)
                        if ch == '$':
                            self.crates.add(pos)
                        if ch == '.':
                            self.targets.add(pos)
                        if ch == '@':
                            self.player = pos
                        if ch == '+':
                            self.player = pos
                            self.targets.add(pos)    
                        if ch == '*':
                            self.crates.add(pos)
                            self.targets.add(pos)
                
                self.bound = maxX, maxY
    
    def gen_state(self):
        return SokobanState(self.player, frozenset(self.crates), frozenset(self.obstacles), frozenset(self.targets))
    
    def gen_game(self):
        return SokobanGame(self.player, self.crates, self.obstacles, self.targets, self.bound)
    
    def get_info(self):
        return self.game_set, self.game_level