import heapq
from collections import deque
from src.core.state import SokobanState

class SokobanAlgorithm:
    def get_full_path(self, solved_state: "SokobanState"):
        if solved_state:
            return_states_path = []
            return_moves_path = []
            current: SokobanState = solved_state
            while current:
                return_states_path = [current] + return_states_path
                if current.prev_move:
                    return_moves_path = [current.prev_move] + return_moves_path
                current = current.parent

            return return_states_path, return_moves_path
        else:
            return [], []
        
    def bfs(self, init_state: "SokobanState"):
        solved_state = None
        visited = set()
        queue = deque([init_state])

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
            return - 15 * len(state.targets)

        crate_to_target_cost = 0
        for crate in state.crates:
            min_dist = min(abs(crate[0] - target[0]) + abs(crate[1] - target[1]) 
                            for target in state.targets)
            crate_to_target_cost += min_dist

        crates_not_on_targets = len(state.crates - state.targets)

        crates_on_targets = len(state.crates & state.targets)

        total_cost = crate_to_target_cost + 10 + crates_not_on_targets - 15 * crates_on_targets
        
        return total_cost
    
    
    def hill_climbing(self, init_state: "SokobanState"):
        solved_state = None
        visited = set()
        # heap: (heuristic_value, counter, state)
        counter = 0  # Tie-breaker counter
        heap = [(self.greedy_cost(init_state), counter, init_state)]

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
                if next_state not in visited and not next_state.is_deadlock():
                    counter += 1
                    heuristic_value = self.greedy_cost(next_state)
                    heapq.heappush(heap, (heuristic_value, counter, next_state))

        return self.get_full_path(solved_state)