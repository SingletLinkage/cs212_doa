import numpy as np
import heapq

G = np.array([[0, 4, 3, float('inf'), float('inf')],
     [4, 0, 1, 2, float('inf')],
     [3, 1, 0, 4, 5],
     [float('inf'), 2, 4, 0, float('inf')],
     [float('inf'), float('inf'), 5, float('inf'), 0]])

available = []
selected = [False]*len(G)
MST = []
minCost = 0

for u in range(len(G)-1):
    for v, w in enumerate(G[u]):
        if v > u:
            heapq.heappush(available, (w, v, u))
    
    while True:
        _w, _v, _u = heapq.heappop(available)
        if not (selected[_v] and selected[_u]):
            selected[_v] = True
            selected[_u] = True
            minCost += _w
            MST.append((_u, _v, _w))
            break

print(MST, minCost)