import numpy as np

DECIMAL_PRECISION = 6

def measure_efficiency_square(length: float = 0, edge: float = 1):
    """
    Measures the efficiency of a road configuration of cities disposed
    in the shape of a square (with a default edge length equal to 1) with a middle, shared road.

    Args:
        length (float): Length of middle shared road (default is 0, for a diagonal disposition)

    Returns:
        float: Average distance between two roads.
        float: Total length of roads.
        float: Quotient of both values which is an efficiency/performance indicator of a road configuration.
    """
    # Define city coordinates (vertices of the square)
    cities = np.array([
        [0, 0],
        [edge, 0],
        [edge, edge],
        [0, edge],
    ])
    
    # Define middle road coordinates (road length [length] can vary)
    mid_road_start = np.array([edge / 2, (edge - length) / 2])
    mid_road_end = np.array([edge / 2, (edge + length) / 2])
    
    # Calculate distances between each pair of cities
    distances = []
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            city_a = cities[i]
            city_b = cities[j]
                        
            # Distance via middle road
            to_mid_start = min(np.linalg.norm(city_a - mid_road_start), np.linalg.norm(city_a - mid_road_end))
            to_mid_end = min(np.linalg.norm(city_b - mid_road_end), np.linalg.norm(city_b - mid_road_start))
            if city_a[0] == city_b[0]:
                distance = to_mid_start + to_mid_end
            else:
                distance = to_mid_start + length + to_mid_end
            
            # Append the distance via middle road
            distances.append(distance)

    # Calculate total road length of roads connected to middle road + middle road itself
    total_road_length = 4 * np.linalg.norm(cities[0] - mid_road_start) + length

    return (
        
        sum(distances) / len(distances),
        total_road_length,
        (sum(distances) / len(distances)) / total_road_length,
    )


if __name__ == "__main__":
    lengths = np.arange(0.3, 0.5, 1/(10 ** DECIMAL_PRECISION))
    
    min_dist = [100, 100]
    for i in lengths:
        avg_dist, total_road, efficiency = measure_efficiency_square(float(i), edge=1)
        # print(i, avg_dist, total_road, efficiency)
        if min_dist == [None, None] or total_road < min_dist[0]:
            min_dist = [total_road, i]
    
    print("Minimum road length:", float(min_dist[0]), "at length:", float(min_dist[1]))