import numpy as np
import time

def read_distance_matrix(file_path):
    # Load the distance matrix from the file
    distance_matrix = np.loadtxt(file_path, delimiter=" ", skiprows=1)
    return distance_matrix
def calculate_total_distance(solution, distance_matrix):
    total_distance = distance_matrix[solution[0], solution[-1]]
    for i in range(len(solution) - 1):
        total_distance += distance_matrix[solution[i], solution[i + 1]]
    return total_distance
def random_solution(n):
    return np.random.permutation(n)

def generate_neighbor_solution(solution, cost, distance):
    neighbor_solution = solution.copy()
    idx1, idx2 = np.random.choice(len(solution), size=2, replace=False)
    neighbor_solution[idx1], neighbor_solution[idx2] = neighbor_solution[idx2], neighbor_solution[idx1]

    # Compute the change in cost due to the swap
    old_cost_idx1 = distance[solution[idx1 - 1]][solution[idx1]] + distance[solution[idx1]][solution[(idx1 + 1) % len(solution)]]
    old_cost_idx2 = distance[solution[idx2 - 1]][solution[idx2]] + distance[solution[idx2]][solution[(idx2 + 1) % len(solution)]]

    new_cost_idx1 = distance[neighbor_solution[idx1 - 1]][neighbor_solution[idx1]] + distance[neighbor_solution[idx1]][neighbor_solution[(idx1 + 1) % len(solution)]]
    new_cost_idx2 = distance[neighbor_solution[idx2 - 1]][neighbor_solution[idx2]] + distance[neighbor_solution[idx2]][neighbor_solution[(idx2 + 1) % len(solution)]]

    # Update the cost based on the changes
    new_cost = cost - old_cost_idx1 - old_cost_idx2 + new_cost_idx1 + new_cost_idx2
    # print(new_cost)
    # print(calculate_total_distance(neighbor_solution, distance))
    return (neighbor_solution, round(new_cost,4))


def sls_with_sa(distance_matrix, max_iterations, initial_temperature = 10, temperature_type='linear', alpha=0.1):
    current_solution = random_solution(len(distance_matrix))
    current_energy = calculate_total_distance(current_solution, distance_matrix)

    if temperature_type == 'exp':
        temperature_schedule = lambda t: initial_temperature * np.exp(-alpha * t)
    elif temperature_type == 'linear':
        temperature_schedule = lambda t: initial_temperature - alpha * t
    else:
        raise ValueError("Invalid temperature_type. Use 'exp' or 'linear'.")

    for t in range(1, max_iterations + 1):
        temperature = temperature_schedule(t)
        # print(temperature)
        if temperature <= 0:
            print("Current iteration = ", t)
            return (current_solution, current_energy)

        (neighbor_solution, neighbor_energy) = generate_neighbor_solution(current_solution, current_energy, distance_matrix)

        energy_difference = neighbor_energy - current_energy

        if energy_difference < 0 or np.random.rand() < np.exp(-energy_difference / temperature):
            current_solution = neighbor_solution
            current_energy = neighbor_energy
    return (current_solution, current_energy)
