import numpy as np

# Define the number of neurons
N = 10 * 10

# Create the Hopfield network class
class HopfieldNetwork:
    def __init__(self, n_neurons):
        self.n_neurons = n_neurons
        self.weights = np.zeros((n_neurons, n_neurons))

    def train(self, patterns):
        for pattern in patterns:
            self.weights += np.outer(pattern, pattern)
        np.fill_diagonal(self.weights, 0)

    def recall(self, pattern, steps=5):
        for _ in range(steps):
            for i in range(self.n_neurons):
                raw_input = np.dot(self.weights[i], pattern)
                pattern[i] = 1 if raw_input > 0 else -1
        return pattern

# Create binary patterns (10x10)
patterns = [
    np.array([
        [-1,  1, -1, -1, -1,  1,  1, -1, -1,  1],
        [ 1, -1,  1,  1, -1, -1, -1,  1,  1, -1],
        [-1,  1,  1, -1,  1, -1,  1, -1,  1, -1],
        [-1, -1,  1, -1, -1,  1, -1, -1,  1,  1],
        [ 1,  1, -1, -1,  1,  1, -1,  1, -1, -1],
        [-1,  1, -1,  1, -1, -1,  1, -1,  1,  1],
        [ 1, -1,  1,  1, -1,  1, -1,  1, -1, -1],
        [-1,  1, -1, -1,  1, -1,  1,  1, -1,  1],
        [ 1, -1,  1, -1, -1, -1,  1,  1, -1,  1],
        [-1,  1, -1,  1,  1, -1, -1,  1,  1, -1]
    ]).flatten()
]

# Initialize the network
hopfield_net = HopfieldNetwork(N)

# Train the network with the patterns
hopfield_net.train(patterns)

# Define a noisy pattern to recall
noisy_pattern = np.array([
    [-1,  1, -1, -1, -1,  1,  1, -1, -1,  1],
    [ 1, -1,  1,  1, -1, -1, -1,  1,  1, -1],
    [-1,  1,  1, -1,  1, -1,  1, -1,  1, -1],
    [-1, -1,  1, -1, -1,  1, -1, -1,  1,  1],
    [ 1,  1, -1, -1,  1,  1, -1,  1, -1, -1],
    [-1,  1, -1,  1, -1, -1,  1, -1,  1,  1],
    [ 1, -1,  1,  1, -1,  1, -1,  1, -1, -1],
    [-1,  1, -1, -1,  1, -1,  1,  1, -1,  1],
    [ 1, -1,  1, -1, -1, -1,  1,  1, -1,  1],
    [-1,  1, -1,  1,  1, -1, -1,  1,  1, -1]
]).flatten()

# Recall the original pattern from the noisy input
recalled_pattern = hopfield_net.recall(noisy_pattern)

# Reshape and print the recalled pattern
print("Recalled Pattern:")
print(recalled_pattern.reshape((10, 10)))
