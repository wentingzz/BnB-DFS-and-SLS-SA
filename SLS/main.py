import numpy as np
import time

def read_distance_matrix(file_path):
    # Load the distance matrix from the file
    distance_matrix = np.loadtxt(file_path, delimiter=" ", skiprows=1)
    return distance_matrix
