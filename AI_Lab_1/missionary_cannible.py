import numpy as np

# Initial and goal states
start_state = [3, 3, 0]  # [Missionaries on left, Cannibals on left, Boat side]
end_state = [0, 0, 1]  # All have crossed to the right side

def possible_actions(current_state):
    m_left, c_left, boat_side = current_state
    valid_states = []
    
    # Possible moves (1 or 2 missionaries/cannibals)
    moves = [
        [-1, 0, 1],  # 1 missionary crosses right
        [-2, 0, 1],  # 2 missionaries cross right
        [0, -1, 1],  # 1 cannibal crosses right
        [0, -2, 1],  # 2 cannibals cross right
        [-1, -1, 1],  # 1 missionary and 1 cannibal cross right
        [1, 0, 0],  # 1 missionary crosses left
        [2, 0, 0],  # 2 missionaries cross left
        [0, 1, 0],  # 1 cannibal crosses left
        [0, 2, 0],  # 2 cannibals cross left
        [1, 1, 0]   # 1 missionary and 1 cannibal cross left
    ]
    
    for move in moves:
        new_state = [m_left + move[0], c_left + move[1], move[2]]
        
        # Validate new state
        if (0 <= new_state[0] <= 3 and 
            0 <= new_state[1] <= 3 and 
            (new_state[0] == 0 or new_state[0] >= new_state[1]) and
            (3 - new_state[0] == 0 or 3 - new_state[0] >= 3 - new_state[1])):
            valid_states.append(new_state)

    return valid_states

class Node:
    def __init__(self, state, parent, cost):
        self.state = state
        self.parent = parent
        self.cost = cost

class Frontier:
    def __init__(self):
        self.nodes = []

    def pop(self):
        return self.nodes.pop(0) if self.nodes else None

    def add(self, node):
        self.nodes.append(node)

    def is_empty(self):
        return len(self.nodes) == 0

    def best_node(self):
        return min(self.nodes, key=lambda n: n.cost, default=None)

class Visited:
    def __init__(self):
        self.visited_states = []

    def add(self, node):
        self.visited_states.append(node.state)

    def contains(self, state):
        return any(np.array_equal(state, visited) for visited in self.visited_states)

def BestFirstSearch(start_state, end_state):
    root_node = Node(start_state, None, 0)
    frontier = Frontier()
    frontier.add(root_node)
    visited = Visited()

    while not frontier.is_empty():
        current_node = frontier.best_node()
        frontier.nodes.remove(current_node)

        if np.array_equal(current_node.state, end_state):
            print("Reached goal state:", current_node.state)
            return

        if visited.contains(current_node.state):
            continue

        visited.add(current_node)
        print("Current State:", current_node.state)

        for action in possible_actions(current_node.state):
            next_node = Node(action, current_node.state, current_node.cost + 1)
            if not visited.contains(next_node.state):
                frontier.add(next_node)

    print("Goal not found.")

if __name__ == "__main__":
    print("=" * 79)
    print("=" * 30 + " Missionaries & Cannibals " + "=" * 30 + "\n")
    BestFirstSearch(start_state, end_state)
    print("=" * 36 + " End " + "=" * 40)
