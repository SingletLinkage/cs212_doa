edges = [(0, 1, 4), (0, 2, 4), (2, 1, 2), (2, 3, 3), (4, 2, 1), (2, 5, 6), (3, 5, 2), (4, 5, 3)]
n = 6
start = 2

graph = []
for u, v, w in edges:
    graph.append((u, v, w))
    graph.append((v, u, w))

distances = [float('inf') for _ in range(n)]
distances[start] = 0

for i in range(n-1):
    for u, v, w in graph:
        if distances[u] != float('inf') and distances[u] + w < distances[v]:
            distances[v] = distances[u] + w

print(distances)