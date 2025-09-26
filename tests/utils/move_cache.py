import json

class Cache:
    def __init__(self, filepath = "tests/utils/move_cache.json"):
        self.filepath = filepath
        self.cache = self.load_cache()

    def load_cache(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def save_cache(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)

    def load_move(self, game_set, game_level, algorithm = None):
        if algorithm:
            moves = self.cache.get(game_set, {}).get(game_level, {}).get(algorithm, [])
        else:
            if len(self.cache.get(game_set, {}).get(game_level, {})) > 0:
                moves = next(iter(self.cache.get(game_set, {}).get(game_level, {}).values()))
            else:
                moves = []
        
        return tuple(tuple(tuple(pos) for pos in move) for move in moves)
    
    def save_move(self, game_set, game_level, algorithm, moves):
        if game_set not in self.cache:
            self.cache[game_set] = {}
        
        if game_level not in self.cache[game_set]:
            self.cache[game_set][game_level] = {}

        pmoves = []

        for move in moves:
            pmoves.append(list(move))

        self.cache[game_set][game_level][algorithm] = pmoves

        self.save_cache()
        