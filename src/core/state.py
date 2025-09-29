from collections import deque

class SokobanState:
    __MOVES = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def __init__(self, player, crates, obstacles, targets, bound, parent: "SokobanState" = None, prev_move = None):
        self.parent = parent
        self.prev_move = prev_move
        
        self.player = player
        self.crates = crates
        self.obstacles = obstacles
        self.targets = targets
        self.bound = bound

    def __eq__(self, value):
        if type(value) is SokobanState:
            return self.player == value.player and self.crates == value.crates and self.obstacles == value.obstacles and self.targets == value.targets
        else:
            return self == value
        
    def __hash__(self):
        return hash((self.player, frozenset(self.crates), frozenset(self.obstacles), frozenset(self.targets)))
    
    def is_deadlock(self):
        return False
    
    def get_reachable(self):
        visited = set()
        queue = deque([self.player])
        visited.add(self.player)  # Mark the starting position as visited
        
        while queue:
            cx, cy = queue.popleft()
            for dx, dy in self.__MOVES:
                next_pos = (cx + dx, cy + dy)
                if next_pos not in visited and next_pos not in self.obstacles and next_pos not in self.crates:
                    queue.append(next_pos)
                    visited.add(next_pos)
        
        return frozenset(visited)

    def get_all_moves(self):
        moves = []
        reachable = self.get_reachable()
        for crate_pos in self.crates:
            cx, cy = crate_pos
            for dx, dy in self.__MOVES:
                near_pos = (cx + dx, cy + dy)
                if near_pos in reachable:
                    ncpos = (cx - dx, cy - dy)
                    if ncpos not in self.obstacles and ncpos not in self.crates:
                        moves.append((near_pos, crate_pos, ncpos))
        
        return moves

    def _get_next_state(self, move):
        _, old_crate_pos, new_crate_pos = move
        
        # Create new crate set efficiently
        new_crates = frozenset((self.crates - {old_crate_pos}) | {new_crate_pos})
        
        return SokobanState(
            player=old_crate_pos,
            crates=new_crates,
            obstacles=self.obstacles,
            targets=self.targets,    
            parent=self,
            prev_move=move,
            bound=self.bound
        )
    
    def get_all_next_states(self):
        moves = self.get_all_moves()
        return [self._get_next_state(move) for move in moves]

    def is_solved(self):
        return self.crates == self.targets