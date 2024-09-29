import random
import math

def simulated_annealing_melody(quality_func, notes, initial_temp, cooling_rate, stopping_temp):
    # Randomly select an initial melody from the available notes
    current_melody = random.sample(notes, len(notes))
    best_melody = current_melody[:]  # Removed invalid syntax
    temperature = initial_temp

    while temperature > stopping_temp:
        # Create a neighboring melody by swapping two notes
        neighbor_melody = current_melody[:]
        i, j = random.sample(range(len(notes)), 2)
        neighbor_melody[i], neighbor_melody[j] = neighbor_melody[j], neighbor_melody[i]

        # Calculate the change in melody quality
        delta_quality = quality_func(neighbor_melody) - quality_func(current_melody)

        if delta_quality < 0 or random.random() < math.exp(-delta_quality / temperature):
            current_melody = neighbor_melody[:]
            if quality_func(current_melody) < quality_func(best_melody):
                best_melody = current_melody[:]

        # Gradually reduce the temperature
        temperature *= cooling_rate

    return best_melody

def quality_func(melody):
    score = 0

    for i in range(len(melody) - 1):
        if melody[i] == 'Sa' and melody[i + 1] != 'Re':
            score += 10
    return score

# Get user input for the notes
user_input = input("Enter the notes for the melody separated by commas: ")
notes = [note.strip() for note in user_input.split(',')]

best_melody = simulated_annealing_melody(quality_func, notes, initial_temp=1000, cooling_rate=0.95, stopping_temp=0.01)
print("Best Melody:", best_melody)