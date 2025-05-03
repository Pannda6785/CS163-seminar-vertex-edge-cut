import threading
import sys
import time
import os
sys.setrecursionlimit(10**7)

current_dir = os.path.dirname(os.path.abspath(__file__))
file_in_path = os.path.join(current_dir, 'S.INP')
file_out_path = os.path.join(current_dir, 'S.OUT')

n = m = 0
adj = []
isBridge = []
isArticulationPoint = []
edges = []
num = []
low = []
bridgeCnt = 0
articulationPointsCnt = 0
timer = 0

def tarjan(u, parent, parentEdgeIdx):
    global timer, bridgeCnt
    num[u] = low[u] = timer
    timer += 1
    children = 0

    for v, edgeIdx in adj[u]:
        if v == parent and edgeIdx == parentEdgeIdx:
            continue
        if num[v] == -1:
            children += 1
            tarjan(v, u, edgeIdx)
            low[u] = min(low[u], low[v])
            if low[v] > num[u]:
                isBridge[edgeIdx] = True
                bridgeCnt += 1
            if parent != -1 and low[v] >= num[u]:
                isArticulationPoint[u] = True
        else:
            low[u] = min(low[u], num[v])
    
    if parent == -1 and children > 1:
        isArticulationPoint[u] = True

def findBridgesAndArticulationPoints():
    global num, low, timer, bridgeCnt, articulationPointsCnt, isBridge, isArticulationPoint
    num = [-1] * n
    low = [0] * n
    timer = 0
    bridgeCnt = 0
    articulationPointsCnt = 0
    isBridge = [False] * m
    isArticulationPoint = [False] * n

    for i in range(n):
        if num[i] == -1:
            tarjan(i, -1, -1)

    articulationPointsCnt = sum(isArticulationPoint)

def main():
    global n, m, adj
    start = time.time()

    with open(file_in_path, "r") as inp:
        n, m = map(int, inp.readline().split())
        adj = [[] for _ in range(n)]
        for i in range(m):
            u, v = map(int, inp.readline().split())
            u -= 1
            v -= 1
            adj[u].append((v, i))
            adj[v].append((u, i))

    findBridgesAndArticulationPoints()

    with open(file_out_path, "w") as out:
        out.write(f"{time.time() - start:.6f}\n")
        out.write(f"{bridgeCnt} {articulationPointsCnt}\n")
        out.write(" ".join(str(i + 1) for i in range(m) if isBridge[i]) + "\n")
        out.write(" ".join(str(i + 1) for i in range(n) if isArticulationPoint[i]) + "\n")

# Run main with a larger stack via thread
threading.stack_size(1 << 27)  # ~128MB stack
thread = threading.Thread(target=main)
thread.start()
thread.join()