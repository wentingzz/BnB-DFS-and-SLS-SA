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
