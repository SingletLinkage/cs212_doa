import heapq

edges = [(0, 1, 4), (0, 2, 4), (2, 1, 2), (2, 3, 3), (4, 2, 1), (2, 5, 6), (3, 5, 2), (4, 5, 3)]
n = 6
start = 2

graph = {i: [] for i in range(n)}
for u, v, w in edges:
    graph[u].append((v, w))
    graph[v].append((u, w))

distances = [float('inf') for _ in range(n)]
distances[start] = 0

pq = [(0, start)]

while pq:
    d, u = heapq.heappop(pq)

    for v, w in graph[u]:
        if distances[v] > distances[u] + w:
            distances[v] = distances[u] + w
            heapq.heappush(pq, (distances[v], v))

print(distances)