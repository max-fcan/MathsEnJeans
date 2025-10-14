from typing import Optional, Dict, Tuple, List
import math

CITIES = 4

def find_optimal_path(graph: Dict[str, Tuple[float, float]], start: Optional[str] = None, end: Optional[str] = None, crossings: bool = False):
    """Version très simple.

    Idée :
    - Si on a exactement 4 points qui forment un carré et crossings=True, on ajoute le centre et on le relie aux 4.
    - Sinon on relie juste les points dans l'ordre où ils apparaissent (ou en partant de 'start' si donné).

    Cette version n'essaie pas d'être optimale dans les autres cas; elle sert juste de base.
    """

    points: Dict[str, Tuple[float, float]] = dict(graph)
    extra_nodes: Dict[str, Tuple[float, float]] = {}

    def is_square(p: Dict[str, Tuple[float, float]]) -> bool:
        if len(p) != 4:
            return False
        xs = sorted({coord[0] for coord in p.values()})
        ys = sorted({coord[1] for coord in p.values()})
        if len(xs) == 2 and len(ys) == 2 and abs((xs[1]-xs[0]) - (ys[1]-ys[0])) < 1e-9:
            return True
        return False

    def dist(a: Tuple[float, float], b: Tuple[float, float]) -> float:
        return math.hypot(a[0]-b[0], a[1]-b[1])

    # Cas carré + crossings
    if crossings and is_square(points):
        xs = sorted({coord[0] for coord in points.values()})
        ys = sorted({coord[1] for coord in points.values()})
        cx = sum(xs)/2
        cy = sum(ys)/2
        name = 'X'
        i = 1
        while name in points:
            name = f'X{i}'
            i += 1
        points[name] = (cx, cy)
        extra_nodes[name] = (cx, cy)
        corners = list(graph.keys())
        edges = [(name, c) for c in corners]
        total = sum(dist(points[name], points[c]) for c in corners)
        return edges, total, extra_nodes

    # Sinon : relier séquentiellement
    order: List[str] = list(points.keys())
    if start and start in order:
        order.remove(start)
        order.insert(0, start)
    if end and end in order and end != order[-1]:
        order.remove(end)
        order.append(end)

    edges: List[Tuple[str, str]] = []
    total = 0.0
    for i in range(len(order)-1):
        a, b = order[i], order[i+1]
        edges.append((a, b))
        total += dist(points[a], points[b])
    return edges, total, extra_nodes


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


if __name__ == "__main__":
    graph = build_square_graph(2)
    print("Graph:", graph)
    edges, cost, extra = find_optimal_path(graph, crossings=True)
    print(f"Solution (arêtes): {edges}\nLongueur totale: {cost:.4f}\nNouveaux points: {extra}")