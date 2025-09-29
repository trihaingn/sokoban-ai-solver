import heapq
from collections import deque

from src.core.state import SokobanState
from src.algorithm.deadlock import DeadlockDetector

class SokobanAlgorithm:
    def __init__(self, state: "SokobanState"):
        self.state = state
        self.deadlock_detector = DeadlockDetector(state)
        self.df = max(state.bound)

    def get_full_path(self, solved_state: "SokobanState"):
        if solved_state:
            return_states_path = []
            return_moves_path = []
            current = solved_state
            while current:
                return_states_path = [current] + return_states_path
                if current.prev_move:
                    return_moves_path = [current.prev_move] + return_moves_path
                current = current.parent

            return return_states_path, return_moves_path
        else:
            return [], []
        
    def bfs(self):
        solved_state = None
        visited = set()
        queue = deque([self.state])

        while queue:
            current = queue.popleft()
            if current.is_solved():
                solved_state = current
                break

            for next_state in current.get_all_next_states():
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append(next_state)
        
        return self.get_full_path(solved_state)
        
    def greedy_cost(self, state: "SokobanState"):
        if state.is_solved():
            return -self.df * len(state.targets)

        crate_to_target_cost = 0
        for crate in state.crates - state.targets:
            min_dist = min(abs(crate[0] - target[0]) + abs(crate[1] - target[1]) 
                            for target in state.targets)
            crate_to_target_cost += min_dist
        
        return crate_to_target_cost + self.df * (len(state.crates - state.targets) - len(state.crates & state.targets))
    
    
    def hybrid_heuristic(self):
        solved_state = None
        visited = set()
        # heap: (heuristic_value, counter, state)
        counter = 0  # Tie-breaker counter
        heap = [(self.greedy_cost(self.state), counter, self.state)]

        while heap:
            # Get the state with the best (lowest) heuristic value
            _, _, current = heapq.heappop(heap)
            
            # Skip if already visited
            if current in visited:
                continue
                
            visited.add(current)
            
            if current.is_solved():
                solved_state = current
                break

            # Generate all possible next states and add to heap
            for next_state in current.get_all_next_states():
                # Check visited and deadlock before adding to heap (more efficient)
                if next_state not in visited and not self.deadlock_detector.is_deadlock(next_state):
                    counter += 1
                    heuristic_value = self.greedy_cost(next_state)
                    heapq.heappush(heap, (heuristic_value, counter, next_state))

        return self.get_full_path(solved_state)