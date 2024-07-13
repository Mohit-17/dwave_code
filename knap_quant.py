from dimod import ConstrainedQuadraticModel, Binary
from dwave.system import LeapHybridCQMSampler
import json


def get_quant_sol(weights,values,capacity):
    # Number of items
    num_items = len(weights)

    # Create the CQM object
    cqm = ConstrainedQuadraticModel()

    # Define the decision variables
    x = [Binary(f"x_{i}") for i in range(num_items)]

    # Objective: Maximize the total value of the items in the knapsack
    cqm.set_objective(-sum(values[i] * x[i] for i in range(num_items)))  # Negative because CQM minimizes by default

    # Constraint: The total weight of the selected items must not exceed the capacity
    cqm.add_constraint(sum(weights[i] * x[i] for i in range(num_items)) <= capacity, label="weight_limit")


    # Solve the problem using a hybrid solver available through Leap
    sampler = LeapHybridCQMSampler()
    sampleset = sampler.sample_cqm(cqm, label="Knapsack Problem Solution")

    # Extracting the best feasible solution
    feasible_solutions = [sample for sample in sampleset.data(fields=['sample', 'energy', 'num_occurrences', 'is_feasible']) if sample.is_feasible]

    if feasible_solutions:
        best_solution = min(feasible_solutions, key=lambda x: x.energy)
        print("Best solution found:")
        for var, value in best_solution.sample.items():
            if value:
                idx = int(var.split("_")[1])
                print(f"Item {idx + 1}: Weight = {weights[idx]}, Value = {values[idx]}")
    else:
        print("No feasible solution found.")

def main():
    with open('instance.json','r') as f:
        data = json.load(f)
    
    weights = data["weights"]
    values = data["profits"]
    capacity = data["max_wgt"]
    get_quant_sol(weights,values,capacity)

if __name__ == "__main__":
    main()