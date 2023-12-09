import time
import numpy as np
import matplotlib.pyplot as plt

global source
source = "../data/10_100.0_10.0.out"

global max_full_path
max_full_path = 1000000


def bnb_dfs(graph):
    N = len(graph)

    upper_bound = []
    heuristic_cost_all = []
    current_cost_all = []
    total_cost_all = []
    best_path = []
    best_cost = np.inf
    nodes_expanded = 0
    full_path = 0

    def nearest_neighbor_bound(graph, current, visited, start):
        n = len(graph)
        heuristic_path = [current]
        local_visited = visited.copy()
        heuristic_cost = 0

        while len(heuristic_path) <= n - len(visited):
            last = heuristic_path[-1]
            next_city = min([(i, graph[last][i]) for i in range(n) if i not in local_visited and i != last],
                            key=lambda x: x[1], default=(None, float('inf')))
            if next_city[0] is None:
                break
            heuristic_path.append(next_city[0])
            heuristic_cost += next_city[1]
            local_visited.add(next_city[0])

        # back to the start node
        heuristic_cost += graph[heuristic_path[-1]][start]

        return heuristic_cost

    t_start = time.time()

    for start in range(N):
        if full_path > max_full_path:
            break

        # initialize
        stack = [(start, [start], 0, set([start]))]

        while stack:
            current, path, cost, visited = stack.pop()

            if len(path) == N:
                complete_cost = cost + graph[current][start]
                if complete_cost < best_cost:
                    best_cost = complete_cost
                    best_path = path + [start]
                full_path += 1
                if full_path > max_full_path:
                    break
                continue

            if cost >= best_cost:
                continue

            nodes_expanded += 1
            upper_bound.append(best_cost)

            for next_city in range(N):
                if next_city not in visited and graph[current][next_city] != np.inf:
                    new_visited = visited.copy()
                    new_visited.add(next_city)
                    current_cost = cost + graph[current][next_city]
                    heuristic_cost = nearest_neighbor_bound(graph, next_city, new_visited, start)
                    if current_cost + heuristic_cost < best_cost:
                        current_cost_all.append(current_cost)
                        heuristic_cost_all.append(heuristic_cost)
                        total_cost_all.append(current_cost + heuristic_cost)
                        stack.append((next_city, path + [next_city], current_cost, new_visited))

    # CPU time
    t_stop = time.time()
    runtime = t_stop - t_start

    # Plots
    fig, axes = plt.subplots(1, 2, figsize=(25, 8))
    fig.tight_layout(pad=8)

    plt.subplot(1, 2, 1)
    plt.plot(upper_bound, linewidth=5)
    plt.title('Path cost', fontsize=20)
    plt.ylabel('Cost', fontsize=20)
    plt.xlabel('Iteration', fontsize=20)

    plt.subplot(1, 2, 2)
    plt.plot(total_cost_all, label="g+h")
    plt.plot(current_cost_all, label="g")
    plt.plot(heuristic_cost_all, label="h")
    plt.title('Cost breakdown', fontsize=20)
    plt.ylabel('Cost', fontsize=20)
    plt.xlabel('Iteration', fontsize=20)
    plt.legend(fontsize=20)

    plt.show()

    return best_path, best_cost, nodes_expanded, runtime


def read_graph():
    f = open(source, "r")
    n = int(f.readline())

    graph = np.ones(n * n).reshape(n, n) * np.inf
    for x in range(n):
        curr_line = f.readline().split(" ")
        for y in range(n):
            if x != y:
                graph[x, y] = curr_line[y]
    return graph, n


def main():
    graph, n = read_graph()
    path, cost, nodes, runtime = bnb_dfs(graph)
    print("Min Cost: {}".format(cost))
    print("Nodes Expanded: {}".format(nodes))
    print("Runtime: {}".format(runtime))
    print("Path: {}".format(path))


if __name__ == '__main__':
    main()
