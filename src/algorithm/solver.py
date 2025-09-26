import heapq
from collections import deque
from src.core.state import SokobanState

class SokobanAlgorithm:
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
                if next_state not in visited and not next_state.is_deadlock():
                    visited.add(next_state)
                    queue.append(next_state)
                    
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
            return None, None
    
    def hill_climbing(self, init_state: "SokobanState"):
        solved_state = None
        visited = set()
        # Priority queue: (heuristic_value, state)
        heap = [(init_state.heuristic_hill_climbing(), init_state)]

        while heap:
            
            # Get the state with the best (lowest) heuristic value
            _, current = heapq.heappop(heap)
            
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
                    heuristic_value = next_state.heuristic_hill_climbing()
                    heapq.heappush(heap, (heuristic_value, next_state))
                    
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
            return None, None
    
    def a_star(self, init_state: "SokobanState"):
        solved_state = None
        # Use closed set for states that have been fully processed
        closed_set = set()
        # Use open set for states to be evaluated
        open_set = set([init_state])
        
        # Priority queue: (f_score, g_score, state_id, state)
        # f_score = g_score + heuristic
        heap = [(init_state.heuristic(), 0, id(init_state), init_state)]
        
        # Cost from start to each state
        g_scores = {init_state: 0}
        
        # For state reconstruction
        came_from = {}

        while heap:
            # Get the state with the best f_score (lowest f = g + h)
            f_score, g_score, state_id, current = heapq.heappop(heap)
            
            # Skip if this state has been processed
            if current in closed_set:
                continue
            
            # Remove from open set and add to closed set
            open_set.discard(current)
            closed_set.add(current)
            
            if current.is_solved():
                solved_state = current
                break

            # Generate all possible next states
            for next_state in current.get_all_next_states():
                # Skip if already fully processed or is a deadlock
                if next_state in closed_set or next_state.is_deadlock():
                    continue
                
                # Calculate tentative g_score
                tentative_g_score = g_score + 1
                
                # If this is a new state or we found a better path
                if (next_state not in g_scores or 
                    tentative_g_score < g_scores[next_state]):
                    
                    # Update the best path to next_state
                    came_from[next_state] = current
                    g_scores[next_state] = tentative_g_score
                    
                    # Calculate f_score with improved heuristic
                    h_score = next_state.heuristic()
                    f_score_new = tentative_g_score + h_score
                    
                    # Add to open set if not already there
                    if next_state not in open_set:
                        open_set.add(next_state)
                        # Use state id to break ties consistently
                        heapq.heappush(heap, (f_score_new, tentative_g_score, id(next_state), next_state))
                    
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
            return None, None