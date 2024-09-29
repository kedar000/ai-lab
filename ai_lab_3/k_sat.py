import random

def generate_k_sat(k, m, n):
    """
    Generate a random k-SAT problem with m clauses and n variables.
   
    Parameters:
        k (int): The number of literals per clause.
        m (int): The number of clauses in the formula.
        n (int): The number of distinct variables.

    Returns:
        clauses (list of lists): A list of m clauses where each clause is a list of k literals.
                                 A literal is represented as an integer, where positive values
                                 indicate the variable and negative values indicate the negation.
    """
    clauses = []
    clause_count = 0

    while clause_count < m:
        clause = set()  # Use a set to ensure distinct literals in each clause
        while True:
            # Randomly choose a variable between 1 and n
            var = random.randint(1, n)
            # Randomly decide if the variable is negated or not
            negated = random.choice([True, False])
            # Add the literal to the clause (negate if needed)
            literal = -var if negated else var
            clause.add(literal)  # Add literal to the clause (set ensures distinct values)
            
            # Break when the clause has k literals
            if len(clause) == k:
                break
        
        clauses.append(list(clause))
        clause_count += 1
   
    return clauses

def print_k_sat(clauses):
    """
    Print the generated k-SAT problem in a readable format.
   
    Parameters:
        clauses (list of lists): The list of clauses to print.
    """
    clause_index = 0
    while True:
        if clause_index >= len(clauses):
            break
        
        clause = clauses[clause_index]
        formatted_clause = " ∨ ".join(f"{'¬' if lit < 0 else ''}x{abs(lit)}" for lit in clause)
        print(f"({formatted_clause})")
        
        clause_index += 1

# Example usage
if __name__ == "__main__":
    # Input parameters
    k = int(input("Enter the value for k (number of literals per clause): "))
    m = int(input("Enter the value for m (number of clauses): "))
    n = int(input("Enter the value for n (number of distinct variables): "))
   
    # Generate k-SAT problem
    k_sat_problem = generate_k_sat(k, m, n)
   
    # Output the generated k-SAT problem
    print("\nGenerated k-SAT problem:")
    print_k_sat(k_sat_problem)
