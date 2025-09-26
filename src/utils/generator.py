import json
from src.core.state import SokobanState
from src.core.game import SokobanGame

class Generator:
    def __init__(self, game_set, game_level):
        with open("src/utils/levels/game.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        _game_set = data.get(game_set, None)
        if not _game_set:
            raise Exception("Level set not found")
        else:
            level_str = _game_set.get(game_level, None)

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
        return SokobanState(self.player, self.crates, self.obstacles, self.targets)
    
    def gen_game(self):
        return SokobanGame(self.player, self.crates, self.obstacles, self.targets, self.bound)