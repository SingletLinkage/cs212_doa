# G = [(u, u, w), ...] where u is a vertex and w is a weight
G = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (2, 4, 5)]
n = 5

def find(p, x):
    if p[x] != x:
        p[x] = find(p, p[x])
    return p[x]

def union(p, r, x, y):
    if r[x] > r[y]:
        p[y] = x
    else:
        p[x] = y
        if r[x] == r[y]:
            r[y] += 1

MST = []
E = sorted(G, key=lambda x: x[2])

p = list(range(n))
r = [0] * n
minCost = 0

for i in range(len(E)):
    u, v, w = E[i]
    x = find(p, u)
    y = find(p, v)

    if x != y:
        MST.append((u, v, w))
        minCost += w
        union(p, r, x, y)
    
print(f'MST: {MST}\nCost: {minCost}')