import numpy as np
from scipy.stats import poisson

# Constants for reduced state space
MAX_BIKES = 10
MAX_MOVE = 3
RENT_REWARD = 10
MOVE_COST = 2
FREE_BIKE_MOVE = 1  # Free bike move
PARKING_COST_THRESHOLD = 10
EXTRA_PARKING_COST = 4
DISCOUNT = 0.9
RENTAL_REQUESTS = [3, 4]
RETURNS = [3, 2]
THRESHOLD = 1e-2

poisson_cache = {}

def poisson_prob(n, lambda_):
    if (n, lambda_) not in poisson_cache:
        poisson_cache[(n, lambda_)] = poisson.pmf(n, lambda_)
    return poisson_cache[(n, lambda_)]

def expected_return(state, action, value_function):
    s1, s2 = state
    effective_action = action - FREE_BIKE_MOVE if action > 0 else action
    s1 -= effective_action
    s2 += effective_action
    s1, s2 = min(MAX_BIKES, max(0, s1)), min(MAX_BIKES, max(0, s2))

    # Moving cost accounting for free transfer
    move_cost = MOVE_COST * max(0, abs(action) - FREE_BIKE_MOVE)
    total_return = -move_cost

    # Parking cost logic
    if s1 > PARKING_COST_THRESHOLD:
        total_return -= EXTRA_PARKING_COST
    if s2 > PARKING_COST_THRESHOLD:
        total_return -= EXTRA_PARKING_COST

    for req1 in range(MAX_BIKES + 1):
        for req2 in range(MAX_BIKES + 1):
            prob_req = poisson_prob(req1, RENTAL_REQUESTS[0]) * poisson_prob(req2, RENTAL_REQUESTS[1])
            rentals1 = min(req1, s1)
            rentals2 = min(req2, s2)
            reward = (rentals1 + rentals2) * RENT_REWARD

            s1_remain = s1 - rentals1
            s2_remain = s2 - rentals2

            for ret1 in range(MAX_BIKES + 1):
                for ret2 in range(MAX_BIKES + 1):
                    prob_ret = poisson_prob(ret1, RETURNS[0]) * poisson_prob(ret2, RETURNS[1])
                    new_s1 = min(s1_remain + ret1, MAX_BIKES)
                    new_s2 = min(s2_remain + ret2, MAX_BIKES)
                    prob = prob_req * prob_ret
                    total_return += prob * (reward + DISCOUNT * value_function[new_s1, new_s2])

    return total_return

def policy_iteration():
    value_function = np.zeros((MAX_BIKES + 1, MAX_BIKES + 1))
    policy = np.zeros((MAX_BIKES + 1, MAX_BIKES + 1), dtype=int)

    is_policy_stable = False
    iteration = 1
    
    while not is_policy_stable:
        print(f"\nPolicy Iteration: {iteration} Starting")
        
        # Policy Evaluation
        while True:
            delta = 0
            new_value_function = np.copy(value_function)
            for s1 in range(MAX_BIKES + 1):
                for s2 in range(MAX_BIKES + 1):
                    action = policy[s1, s2]
                    new_value_function[s1, s2] = expected_return((s1, s2), action, value_function)
                    delta = max(delta, abs(new_value_function[s1, s2] - value_function[s1, s2]))
            
            value_function = new_value_function
            
            print(f"  Evaluating Policy... Max Delta: {delta:.6f}")
            if delta < THRESHOLD:
                print("  Policy Evaluation Converged")
                break
        
        # Policy Improvement
        is_policy_stable = True
        print("  Improving Policy...")
        for s1 in range(MAX_BIKES + 1):
            for s2 in range(MAX_BIKES + 1):
                old_action = policy[s1, s2]
                action_returns = [
                    expected_return((s1, s2), action, value_function) if 0 <= s1 - (action - FREE_BIKE_MOVE) <= MAX_BIKES and 0 <= s2 + (action - FREE_BIKE_MOVE) <= MAX_BIKES else float('-inf')
                    for action in range(-MAX_MOVE, MAX_MOVE + 1)
                ]
                policy[s1, s2] = np.argmax(action_returns) - MAX_MOVE
                if old_action != policy[s1, s2]:
                    is_policy_stable = False
        
        print(f"Policy Iteration {iteration} Complete - Policy Stable: {is_policy_stable}")
        iteration += 1
    
    return policy, value_function

if __name__ == "__main__":
    print("Starting Policy Iteration for Enhanced Gbike Problem...")
    policy, value_function = policy_iteration()
    print("Policy Iteration Completed Successfully!")
    print("\nOptimal Policy:")
    print(policy)
    print("\nValue Function:")
    print(value_function)