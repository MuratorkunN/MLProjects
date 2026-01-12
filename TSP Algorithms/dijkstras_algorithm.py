def get_min_distance(distances, visited):
    min_dist = float('inf')
    min_index = -1

    for i in range(len(distances)):
        if not visited[i] and distances[i] < min_dist:
            min_dist = distances[i]
            min_index = i

    return min_index


def dijkstra(nodes, distance_matrix, start):
    num_vertices = len(nodes)
    distances = [float('inf')] * num_vertices
    visited = [False] * num_vertices

    distances[start] = 0

    for _ in range(num_vertices):
        # unvisited node with the smallest distance
        u = get_min_distance(distances, visited)

        # reachable node not found or all remaining are infinity
        if u == -1:
            break

        visited[u] = True

        # updatin neighbors of u
        for v in range(num_vertices):
            weight = distance_matrix[u][v]

            #  if edge exists and needs update
            if weight is not None and weight != float('inf'):
                if not visited[v] and distances[u] != float('inf'):
                    new_dist = distances[u] + weight
                    if new_dist < distances[v]:
                        distances[v] = new_dist

    return distances


"""
nodes = ["n1", "n2", "n3", "n4", "n5"]

inf = float('inf')

distance = [
    [0,   6,   inf, 1,   inf],
    [6,   0,   5,   2,   2],
    [inf, 5,   0,   inf, 5],
    [1,   2,   inf, 0,   1],
    [inf, 2,   5,   1,   0],
]

start = 0

distances = dijkstra(nodes, distance, start)

print(f"from {nodes[start]}")
for i, d in enumerate(distances):
    print(f"distance to {nodes[i]}: {d}")

expected = [0, 3, 7, 1, 2]
if distances == expected:
    print("\ncorrect")
"""