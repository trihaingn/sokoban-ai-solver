from collections import deque

from src.core.state import SokobanState

class DeadlockDetector:
    __MOVES = ((0,1),(1,0),(0,-1),(-1,0))
    def __init__(self, init_state: "SokobanState"):
        maxX, maxY = init_state.bound
        self.free_squares = frozenset(((x,y) for x in range(maxX) for y in range(maxY))) - init_state.obstacles
        box_reachable = set()

        for target in init_state.targets:
            box_reachable.add(target)
            queue = deque([target])

            while queue:
                cur_pos = queue.popleft()
                cx, cy = cur_pos

                for dx, dy in self.__MOVES:
                    prev_crate_pos = (cx + dx), (cy + dy)
                    prev_player_pos = (cx + 2 * dx), (cy + 2 * dy)

                    if (prev_player_pos not in init_state.obstacles and prev_crate_pos not in box_reachable and prev_crate_pos not in init_state.obstacles):
                        box_reachable.add(prev_crate_pos)
                        queue.append(prev_crate_pos)

        self.dead_squares = frozenset(self.free_squares - box_reachable)
    
    def cannot_push(self, state: "SokobanState", crate: tuple[int, int], visited: set) -> bool:
        if (crate in visited):
            return True
        
        visited.add(crate)
        cx, cy = crate
        right, down, left, up = (cx, cy + 1), (cx + 1, cy), (cx, cy - 1), (cx - 1, cy)

        return (((right in state.obstacles or left in state.obstacles) or 
                        (right in self.dead_squares and left in self.dead_squares) or 
                        ((right in state.crates and self.cannot_push(state,right, visited)) or (left in state.crates and self.cannot_push(state, left, visited))))
                    and ((up in state.obstacles or down in state.obstacles) or 
                        (up in self.dead_squares and down in self.dead_squares) or 
                        ((up in state.crates and self.cannot_push(state, up, visited)) or (down in state.crates and self.cannot_push(state, down, visited)))))      

    def is_deadlock(self, state: "SokobanState"):
        for crate in state.crates - state.targets:
            if crate in self.dead_squares:
                return True
            
            if (self.cannot_push(state, crate, set())):
                return True
            
        
        return False

