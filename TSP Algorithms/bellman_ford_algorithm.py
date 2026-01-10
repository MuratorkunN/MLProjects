def bellman_ford(nodes, matrix, start):
    num_vertices = len(nodes)
    # initial distances = infinity except source = 0
    distances = [float('inf')] * num_vertices
    distances[start] = 0

    # |V| - 1 iterations
    for _ in range(num_vertices - 1):
        for u in range(num_vertices):
            for v in range(num_vertices):
                weight = matrix[u][v]

                # if there is an edge
                if weight is not None and weight != float('inf'):
                    # old vs new comparison
                    if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight

    # negative cycles check
    for u in range(num_vertices):
        for v in range(num_vertices):
            weight = matrix[u][v]
            if weight is not None and weight != float('inf'):
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    # we can still reduce distance = there is a negative cycle
                    raise ValueError("negative cycle!")

    return distances