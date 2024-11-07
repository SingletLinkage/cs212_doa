G = [...]
ST = [...]

def is_spanning_tree(G, ST):
    vertices = set()
    for u, v, w in G:
        vertices.add(u)
        vertices.add(v)
    
    if len(vertices) != len(ST) + 1:
        print('Invalid Spanning Tree')
        return False
    
    p = {v: v for v in vertices}
    rank = {v: 0 for v in vertices}
    
    def find(p, x):
        if p[x] != x:
            p[x] = find(p, p[x])
        return p[x]

    def union(p, rank, u, v):
        x = find(p, u)
        y = find(p, v)
        
        if x != y:
            if rank[x] > rank[y]:
                p[y] = x
            elif rank[x] < rank[y]:
                p[x] = y
            else:
                p[y] = x
                rank[x] += 1
            return True
        return False

    for u, v, w in ST:
        if (u, v, w) not in G and (v, u, w) not in G:
            print('Invalid Spanning Tree')
            return False
        if not union(p, rank, u, v):
            print('Invalid Spanning Tree')
            return False


