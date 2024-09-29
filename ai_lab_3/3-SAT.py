import random

# Helper function to evaluate a solution (count unsatisfied clauses)
def evaluate_solution(solution, clauses):
    unsatisfied = 0
    for clause in clauses:
        if not any((lit > 0 and solution[abs(lit) - 1]) or (lit < 0 and not solution[abs(lit) - 1]) for lit in clause):
            unsatisfied += 1
    return unsatisfied

# Randomly generate an initial solution
def random_solution(n):
    return [random.choice([True, False]) for _ in range(n)]

# Hill-Climbing Algorithm
def hill_climbing(clauses, n, max_iterations=1000):
    current_solution = random_solution(n)
    current_score = evaluate_solution(current_solution, clauses)
   
    iterations = 0
    while True:
        if current_score == 0 or iterations >= max_iterations:
            break
       
        # Try flipping each variable to find the best neighbor
        best_neighbor = current_solution
        best_score = current_score
        i = 0
        while i < n:
            neighbor = current_solution[:]
            neighbor[i] = not neighbor[i]  # Flip the variable
            neighbor_score = evaluate_solution(neighbor, clauses)
           
            if neighbor_score < best_score:
                best_neighbor = neighbor
                best_score = neighbor_score
            i += 1
       
        if best_score >= current_score:  # No improvement
            break
       
        current_solution = best_neighbor
        current_score = best_score
        iterations += 1
   
    return current_solution, current_score

# Beam Search Algorithm
def beam_search(clauses, n, beam_width=3, max_iterations=1000):
    candidates = [random_solution(n) for _ in range(beam_width)]
    candidate_scores = [evaluate_solution(candidate, clauses) for candidate in candidates]
   
    iterations = 0
    while True:
        if min(candidate_scores) == 0 or iterations >= max_iterations:
            break
       
        # Generate neighbors for all beam candidates
        new_candidates = []
        for candidate in candidates:
            i = 0
            while i < n:
                neighbor = candidate[:]
                neighbor[i] = not neighbor[i]  # Flip the variable
                new_candidates.append(neighbor)
                i += 1
       
        # Keep the best 'beam_width' candidates
        new_scores = [evaluate_solution(candidate, clauses) for candidate in new_candidates]
        sorted_candidates = sorted(zip(new_scores, new_candidates))[:beam_width]
        candidates = [candidate for _, candidate in sorted_candidates]
        candidate_scores = [evaluate_solution(candidate, clauses) for candidate in candidates]
        iterations += 1
   
    return candidates[0], min(candidate_scores)

# Variable-Neighborhood Descent (VND)
def variable_neighborhood_descent(clauses, n, max_iterations=1000):
    current_solution = random_solution(n)
    current_score = evaluate_solution(current_solution, clauses)
   
    neighborhood_functions = [
        lambda sol: [flip_random(sol, n) for _ in range(n)],   # Neighborhood 1: Random flips
        lambda sol: [flip_two_random(sol, n) for _ in range(n)],# Neighborhood 2: Flip two random variables
        lambda sol: [swap_two_random(sol, n) for _ in range(n)] # Neighborhood 3: Swap values of two random variables
    ]
   
    iterations = 0
    while True:
        if current_score == 0 or iterations >= max_iterations:
            break
       
        for neighborhood_fn in neighborhood_functions:
            neighbors = neighborhood_fn(current_solution)
            best_neighbor = min(neighbors, key=lambda sol: evaluate_solution(sol, clauses))
            best_score = evaluate_solution(best_neighbor, clauses)
           
            if best_score < current_score:
                current_solution = best_neighbor
                current_score = best_score
                break
        iterations += 1
   
    return current_solution, current_score

# Neighborhood function helpers for VND
def flip_random(solution, n):
    neighbor = solution[:]
    i = random.randint(0, n - 1)
    neighbor[i] = not neighbor[i]
    return neighbor

def flip_two_random(solution, n):
    neighbor = solution[:]
    i, j = random.sample(range(n), 2)
    neighbor[i] = not neighbor[i]
    neighbor[j] = not neighbor[j]
    return neighbor

def swap_two_random(solution, n):
    neighbor = solution[:]
    i, j = random.sample(range(n), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

# Heuristic function to count unsatisfied clauses
def heuristic_unsatisfied_clauses(solution, clauses):
    return evaluate_solution(solution, clauses)

# Heuristic function for clause satisfaction score
def heuristic_clause_satisfaction(solution, clauses):
    satisfied_clauses = sum(any((lit > 0 and solution[abs(lit) - 1]) or (lit < 0 and not solution[abs(lit) - 1]) for lit in clause) for clause in clauses)
    return satisfied_clauses

# Generate a random 3-SAT problem
def generate_3_sat(m, n):
    return [[random.choice([i + 1, -(i + 1)]) for i in random.sample(range(n), 3)] for _ in range(m)]

# Compare performance of different algorithms on random 3-SAT problems
def compare_algorithms():
    n = 10  # Number of variables
    m = 20  # Number of clauses
   
    clauses = generate_3_sat(m, n)
   
    print("3-SAT problem clauses:")
    for clause in clauses:
        print(clause)
   
    # Hill Climbing
    hc_solution, hc_score = hill_climbing(clauses, n)
    print("\nHill-Climbing Solution:", hc_solution)
    print("Unsatisfied Clauses:", hc_score)
   
    # Beam Search (beam width 3)
    bs_solution, bs_score = beam_search(clauses, n, beam_width=3)
    print("\nBeam Search (width 3) Solution:", bs_solution)
    print("Unsatisfied Clauses:", bs_score)
   
    # Beam Search (beam width 4)
    bs_solution_4, bs_score_4 = beam_search(clauses, n, beam_width=4)
    print("\nBeam Search (width 4) Solution:", bs_solution_4)
    print("Unsatisfied Clauses:", bs_score_4)
   
    # Variable-Neighborhood Descent (VND)
    vnd_solution, vnd_score = variable_neighborhood_descent(clauses, n)
    print("\nVariable-Neighborhood Descent Solution:", vnd_solution)
    print("Unsatisfied Clauses:", vnd_score)

# Run the comparison
if __name__ == "__main__":
    compare_algorithms()
