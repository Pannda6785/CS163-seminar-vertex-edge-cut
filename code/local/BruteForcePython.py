import time
import sys
import os
from collections import defaultdict

sys.setrecursionlimit(10**7)
current_dir = os.path.dirname(os.path.abspath(__file__))
file_in_path = os.path.join(current_dir, 'S.INP')
file_out_path = os.path.join(current_dir, 'S.OUT')

def dfs(u, adj, visited, forbidden, ignore_edge):
    visited[u] = True
    for v in adj[u]:
        if forbidden[v] or visited[v]:
            continue
        if ignore_edge != (-1, -1):
            if (min(u, v), max(u, v)) == ignore_edge:
                continue
        dfs(v, adj, visited, forbidden, ignore_edge)

def count_components(adj, forbidden, ignore_edge):
    n = len(adj)
    visited = [False] * n
    components = 0
    for i in range(n):
        if not forbidden[i] and not visited[i]:
            dfs(i, adj, visited, forbidden, ignore_edge)
            components += 1
    return components

start = time.time()

with open(file_in_path, "r") as f:
    lines = f.read().splitlines()

n, m = map(int, lines[0].split())
adj = [[] for _ in range(n)]
edges = []

for i in range(1, m + 1):
    u, v = map(int, lines[i].split())
    u -= 1
    v -= 1
    adj[u].append(v)
    adj[v].append(u)
    edges.append((min(u, v), max(u, v)))

k = count_components(adj, [False] * n, (-1, -1))

bridges = []
for i in range(m):
    e = edges[i]
    comp = count_components(adj, [False] * n, e)
    if comp > k:
        bridges.append(i + 1) 

articulation_points = []
for i in range(n):
    forbidden = [False] * n
    forbidden[i] = True
    comp = count_components(adj, forbidden, (-1, -1))
    if comp > k:
        articulation_points.append(i + 1) 

with open(file_out_path, "w") as f:
    f.write(f"{time.time() - start:.6f}\n")
    f.write(f"{len(bridges)} {len(articulation_points)}\n")
    f.write(" ".join(map(str, sorted(bridges))) + "\n")
    f.write(" ".join(map(str, sorted(articulation_points))) + "\n")
