import copy
from collections import deque

class SokobanState:
    __MOVES = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def __init__(self, player, crates, obstacles, targets, parent: "SokobanState" = None, prev_move = None):
        self.parent = parent
        self.prev_move = prev_move
        
        self.player = player
        self.crates = crates
        self.obstacles = obstacles
        self.targets = targets
            
    def __eq__(self, value):
        if type(value) is SokobanState:
            return self.player == value.player and self.crates == value.crates and self.obstacles == value.obstacles and self.targets == value.targets
        else:
            return self == value
        
    def __hash__(self):
        return hash((self.player, frozenset(self.crates), frozenset(self.obstacles), frozenset(self.targets)))
    
    def __lt__(self, other):
        return self.heuristic() < other.heuristic()
    
    def heuristic(self):
        if self.is_solved():
            return 0
        
        total_manhattan = 0
        for crate in self.crates:
            if self.targets:
                min_dist = min(abs(crate[0] - target[0]) + abs(crate[1] - target[1]) 
                             for target in self.targets)
                total_manhattan += min_dist

        misplaced_crates = len(self.crates - self.targets)

        return max(total_manhattan, misplaced_crates)
    
    def heuristic_hill_climbing(self):
        if self.is_solved():
            return 0
        
        total_cost = 0
        
        crate_to_target_cost = 0
        for crate in self.crates:
            if self.targets:
                min_dist = min(abs(crate[0] - target[0]) + abs(crate[1] - target[1]) 
                             for target in self.targets)
                crate_to_target_cost += min_dist
        
        crates_not_on_targets = len(self.crates - self.targets)
        not_on_target_penalty = crates_not_on_targets * 10
        
        player_to_crate_cost = 0
        if self.crates:
            min_player_dist = min(abs(self.player[0] - crate[0]) + abs(self.player[1] - crate[1]) 
                                for crate in self.crates)
            player_to_crate_cost = min_player_dist * 0.1
        
        crates_on_targets = len(self.crates & self.targets)
        on_target_bonus = -crates_on_targets * 15
        
        total_cost = crate_to_target_cost + not_on_target_penalty + player_to_crate_cost + on_target_bonus
        
        return total_cost
    
    def is_deadlock(self):
        return False
    
    def get_reachable(self):
        visited = set()
        queue = deque([self.player])
        while queue:
            cx, cy = queue.popleft()
            for dx, dy in self.__MOVES:
                next_pos = (cx + dx, cy + dy)
                if next_pos not in visited and next_pos not in self.obstacles and next_pos not in self.crates:
                    queue.append(next_pos)
                    visited.add(next_pos)
        
        return visited

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
        next_state = copy.deepcopy(self)

        _, next_ppos, next_cpos = move
        
        next_state.crates.remove(next_ppos)
        next_state.crates.add(next_cpos)

        next_state.player = next_ppos

        next_state.parent = self
        next_state.prev_move = move

        return next_state
    
    def get_all_next_states(self):
        moves = self.get_all_moves()
        return [self._get_next_state(move) for move in moves]

    def is_solved(self):
        return self.crates == self.targets