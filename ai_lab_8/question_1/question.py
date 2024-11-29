import numpy as np

def value_iteration(grid, actions, rewards, transition_probs, discount_factor, threshold):
    """Perform value iteration to find the optimal policy."""
    value_function = np.zeros_like(grid, dtype=float)
    policy = np.zeros_like(grid, dtype=int)

    while True:
        delta = 0
        new_value_function = value_function.copy()

        for x in range(grid.shape[0]):
            for y in range(grid.shape[1]):
                if (x, y) in rewards:  # Skip terminal states
                    continue

                v = value_function[x, y]
                action_values = []

                for action, direction in actions.items():
                    value = 0
                    for prob, (dx, dy) in transition_probs[action]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]:
                            value += prob * (rewards.get((nx, ny), -0.04) + discount_factor * value_function[nx, ny])
                        else:
                            value += prob * (rewards.get((x, y), -0.04) + discount_factor * value_function[x, y])
                    action_values.append(value)

                new_value_function[x, y] = max(action_values)
                policy[x, y] = np.argmax(action_values)

                delta = max(delta, abs(v - new_value_function[x, y]))

        value_function = new_value_function

        if delta < threshold:
            break

    return value_function, policy

# Define the 4x3 grid and parameters
grid = np.zeros((4, 3))
rewards = {
    (3, 2): 1,  # Terminal state +1
    (3, 1): -1  # Terminal state -1
}
actions = {
    0: (-1, 0),  # Up
    1: (1, 0),   # Down
    2: (0, -1),  # Left
    3: (0, 1)    # Right
}

# Define transition probabilities for stochastic environment
transition_probs = {
    0: [(0.8, (-1, 0)), (0.1, (0, -1)), (0.1, (0, 1))],  # Up
    1: [(0.8, (1, 0)), (0.1, (0, -1)), (0.1, (0, 1))],   # Down
    2: [(0.8, (0, -1)), (0.1, (-1, 0)), (0.1, (1, 0))],  # Left
    3: [(0.8, (0, 1)), (0.1, (-1, 0)), (0.1, (1, 0))]    # Right
}

# Set parameters
discount_factor = 0.9
threshold = 1e-4

# Solve the problem for r(s) = -2
for state in grid.flat:
    if state not in rewards:
        rewards[(state)] = -2

value_function, policy = value_iteration(grid, actions, rewards, transition_probs, discount_factor, threshold)

# Print results
# print("Optimal Value Function:")
# print(value_function)
# print("\nOptimal Policy (0:Up, 1:Down, 2:Left, 3:Right):")
# print(policy)
# Print results
print("Optimal Value Function:")
for x in range(grid.shape[0]):
    for y in range(grid.shape[1]):
        if (x, y) in rewards:  # Display terminal state rewards
            print(f"{rewards[(x, y)]:.2f}", end="\t")
        else:
            print(f"{value_function[x, y]:.2f}", end="\t")
    print()

print("\nOptimal Policy (0:Up, 1:Down, 2:Left, 3:Right):")
print(policy)