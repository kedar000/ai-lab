from queue import PriorityQueue
import copy

# Initial board configuration
initial_board = [
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, -1, 1, 1, 1, -1, -1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, -1, 1, 1, 1, -1, -1]
]

# Goal board configuration
goal_board = [
    [-1, -1, 0, 0, 0, -1, -1],
    [-1, -1, 0, 0, 0, -1, -1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [-1, -1, 0, 0, 0, -1, -1],
    [-1, -1, 0, 0, 0, -1, -1]
]

# Directions for valid moves
directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # Up, down, left, right


# 1. Check if a move is valid (jump over a marble into an empty space)
def is_valid_move(board, x, y, dx, dy):
    if 0 <= x + dx < 7 and 0 <= y + dy < 7 and board[x][y] == 1 and board[x + dx][y + dy] == 0:
        mid_x, mid_y = x + dx // 2, y + dy // 2
        return board[mid_x][mid_y] == 1  # Ensure there's a marble to jump over
    return False


# 2. Apply the move and return a new board configuration
def apply_move(board, x, y, dx, dy):
    new_board = copy.deepcopy(board)
    new_board[x][y] = 0  # Current position becomes empty
    new_board[x + dx // 2][y + dy // 2] = 0  # The jumped marble is removed
    new_board[x + dx][y + dy] = 1  # Move to the new position
    return new_board


# Heuristic 1: Count the remaining marbles (fewer marbles is better)
def count_marbles(board):
    return sum(row.count(1) for row in board)


# Heuristic 2: Calculate the Manhattan distance of all marbles from the center (closer to center is better)
def distance_to_center(board):
    center_x, center_y = 3, 3
    distance = 0
    for x in range(7):
        for y in range(7):
            if board[x][y] == 1:
                distance += abs(x - center_x) + abs(y - center_y)
    return distance


# 3. Priority Queue based search (can be used for Best-First or A*)
def priority_queue_search(start_board, heuristic_fn, use_path_cost=False):
    pq = PriorityQueue()
    visited = set()
    pq.put((0, start_board, 0))  # (priority, board, path_cost)

    while not pq.empty():
        priority, board, path_cost = pq.get()

        # If the goal is reached (1 marble in the center)
        if count_marbles(board) == 1 and board[3][3] == 1:
            return path_cost  # Return the number of moves

        board_tuple = tuple(map(tuple, board))
        if board_tuple in visited:
            continue
        visited.add(board_tuple)

        for x in range(7):
            for y in range(7):
                for dx, dy in directions:
                    if is_valid_move(board, x, y, dx, dy):
                        new_board = apply_move(board, x, y, dx, dy)
                        new_path_cost = path_cost + 1

                        # Priority based on heuristic or both heuristic and path cost (for A*)
                        new_priority = heuristic_fn(new_board)
                        if use_path_cost:
                            new_priority += new_path_cost  # A* uses g(n) + h(n)

                        pq.put((new_priority, new_board, new_path_cost))

    return None  # No solution


# 4. Best First Search using Heuristic 1 (number of remaining marbles)
def best_first_search(board):
    return priority_queue_search(board, count_marbles, use_path_cost=False)


# 5. A* Search using Heuristic 2 (distance to center + path cost)
def a_star_search(board):
    return priority_queue_search(board, distance_to_center, use_path_cost=True)


# Compare Best-First Search and A* Search
if __name__ == "__main__":
    best_first_result = best_first_search(initial_board)
    a_star_result = a_star_search(initial_board)

    print(f"Best-First Search result: {best_first_result} moves")
    print(f"A* Search result: {a_star_result} moves")
