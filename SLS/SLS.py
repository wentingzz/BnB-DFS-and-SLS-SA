import numpy as np
import time
import matplotlib.pyplot as plt

global total_cost_all
total_cost_all = []

global temperature_all
temperature_all = []


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
    old_cost_idx1 = distance[solution[idx1 - 1]][solution[idx1]] + \
                    distance[solution[idx1]][solution[(idx1 + 1) % len(solution)]]
    old_cost_idx2 = distance[solution[idx2 - 1]][solution[idx2]] + \
                    distance[solution[idx2]][solution[(idx2 + 1) % len(solution)]]

    new_cost_idx1 = distance[neighbor_solution[idx1 - 1]][neighbor_solution[idx1]] + \
                    distance[neighbor_solution[idx1]
                    ][neighbor_solution[(idx1 + 1) % len(solution)]]
    new_cost_idx2 = distance[neighbor_solution[idx2 - 1]][neighbor_solution[idx2]] + \
                    distance[neighbor_solution[idx2]
                    ][neighbor_solution[(idx2 + 1) % len(solution)]]

    # Update the cost based on the changes
    new_cost = cost - old_cost_idx1 - old_cost_idx2 + new_cost_idx1 + new_cost_idx2
    # print(new_cost)
    # print(calculate_total_distance(neighbor_solution, distance))
    return (neighbor_solution, round(new_cost, 4))


def sls_with_sa(distance_matrix, max_iterations, initial_temperature=10, temperature_type='linear', alpha=0.1):
    current_solution = random_solution(len(distance_matrix))
    current_energy = calculate_total_distance(
        current_solution, distance_matrix)

    if temperature_type == 'exp':
        def temperature_schedule(
                t):
            return initial_temperature * np.exp(-alpha * t)
    elif temperature_type == 'linear':
        def temperature_schedule(t):
            return initial_temperature - alpha * t
    else:
        raise ValueError("Invalid temperature_type. Use 'exp' or 'linear'.")

    for t in range(1, max_iterations + 1):
        temperature = temperature_schedule(t)
        # print(temperature)
        if temperature <= 0:
            print("Current iteration = ", t)
            # return (current_solution, current_energy)
            break

        (neighbor_solution, neighbor_energy) = generate_neighbor_solution(
            current_solution, current_energy, distance_matrix)

        energy_difference = neighbor_energy - current_energy

        if energy_difference < 0 or np.random.rand() < np.exp(-energy_difference / temperature):
            current_solution = neighbor_solution
            current_energy = neighbor_energy
            total_cost_all.append(current_energy)
            temperature_all.append(temperature)
    return (current_solution, current_energy)


def draw_details():
    fig, axes = plt.subplots(1, 2, figsize=(25, 8))
    fig.tight_layout(pad=8)

    plt.subplot(1, 2, 1)
    plt.plot(total_cost_all, linewidth=5)
    plt.title('Path cost', fontsize=20)
    plt.ylabel('Cost', fontsize=20)
    plt.xlabel('Iteration', fontsize=20)

    plt.subplot(1, 2, 2)
    plt.plot(temperature_all, linewidth=5, color='red')
    plt.title('Temperature changes', fontsize=20)
    plt.ylabel('Temperature', fontsize=20)
    plt.xlabel('Iteration', fontsize=20)

    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # file = input("Enter the TSP distance file: ")
    # max_iteration = int(input("Enter the number of maximal iterations: "))
    # init_tmp = int(input("Enter initial temperature: "))
    file = "../data/200_100.0_10.0.out"
    max_iteration = 100000
    initial_temperature = 10
    temperature_type = 'exp'
    alpha = 0.0001
    distance = read_distance_matrix(file)

    start_time = time.time()
    sol, cost = sls_with_sa(distance, max_iteration,
                            initial_temperature, temperature_type, alpha)
    end_time = time.time()
    print(sol)
    # Calculate and print the runtime
    runtime = end_time - start_time
    print("Runtime:", round(runtime, 4), "seconds")
    print(cost)

    draw_details()