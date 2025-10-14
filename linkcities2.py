from typing import Optional

CITIES = 4

def find_optimal_path(graph, start: Optional[str], end: Optional[str], crossings=False):
    """
    Finds the optimal path passing through all the nodes in a graph, optionally starting from start and end nodes in the graph, optionally has crossings.

    :param graph: A dictionary representing the graph with node coordinates.
    :param start: The starting node.
    :param end: The ending node.
    :param crossings: Whether to allow crossings in the path.
    :return: A tuple containing the optimal path and its cost.
    """

    from itertools import permutations
    import math

    def euclidean_distance(a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    nodes = list(graph.keys())
    if start and start in nodes:
        nodes.remove(start)
        nodes.insert(0, start)
    if end and end in nodes:
        nodes.remove(end)
        nodes.append(end)

    min_cost = float('inf')
    best_path = []

    for perm in permutations(nodes[1:-1] if start and end else nodes):
        path = [nodes[0]] + list(perm) + ([nodes[-1]] if end else [])
        cost = sum(euclidean_distance(graph[path[i]], graph[path[i + 1]]) for i in range(len(path) - 1))
        
        if cost < min_cost:
            min_cost = cost
            best_path = path

    return best_path, min_cost

def build_square_graph(size):
    """
    Builds a square graph with given size.
    
    :param size: The size of the square graph (number of nodes on one side).
    :return: A dictionary representing the graph with coordinates.
    """
    graph = {}
    for i in range(size):
        for j in range(size):
            node = chr(65 + i * size + j)  # Convert to letters A, B, C, ...
            graph[node] = (i, j)
    return graph

def build_rect_graph(size):
    """
    Builds a square graph with given size.
    
    :param size: The size of the square graph (number of nodes on one side).
    :return: A dictionary representing the graph with coordinates.
    """
    graph = {}
    for i in range(size):
        for j in range(size+3):
            node = chr(65 + i * size + j)  # Convert to letters A, B, C, ...
            graph[node] = (i, j)
    return graph


if __name__ == "__main__":
    graph = build_square_graph(2)
    print("Graph:", graph)
    start = 'A'
    end = 'D'
    path, cost = find_optimal_path(graph, start, end)
    print(f"Optimal path: {path} with cost: {cost}")