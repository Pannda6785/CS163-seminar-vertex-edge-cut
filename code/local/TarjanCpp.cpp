#include <iostream>
#include <vector>
#include <ctime>

using namespace std;

int n, m;
vector<vector<pair<int, int>>> adj;
vector<bool> isBridge, isArticulationPoint;
vector<pair<int, int>> edges;
vector<int> num, low;
int bridgeCnt, articulationPointsCnt, timer;

void tarjan(int u, int parent, int parentEdgeIdx) {
    num[u] = low[u] = timer++;
    int children = 0;
    for (pair<int, int> x : adj[u]) {
        int v = x.first;
        int edgeIdx = x.second;
        if (v == parent && edgeIdx == parentEdgeIdx) continue;
        if (num[v] == -1) { // Unvisited
            children++;
            tarjan(v, u, edgeIdx);
            low[u] = min(low[u], low[v]);
            if (low[v] > num[u]) { // Bridge condition
                isBridge[edgeIdx] = true;
                bridgeCnt++;
            }
            if (parent != -1 && low[v] >= num[u]) { // Non-root articulation point
                isArticulationPoint[u] = true;
            }
        } else { // Back edge
            low[u] = min(low[u], num[v]);
        }
    }

    if (parent == -1 && children > 1) { // Root with multiple children
        isArticulationPoint[u] = true;
    }
}

void findBridgesAndArticulationPoints() {
    num.assign(n, -1);
    low.assign(n, 0);
    timer = 0;
    bridgeCnt = articulationPointsCnt = 0;
    isBridge.assign(m, false);
    isArticulationPoint.assign(n, false);
    for (int i = 0; i < n; i++) {
        if (num[i] == -1) tarjan(i, -1, -1);
    }
    // Count articulation points
    for (int i = 0; i < n; i++) {
        if (isArticulationPoint[i]) articulationPointsCnt++;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    freopen("S.INP", "r", stdin);
    freopen("S.OUT", "w", stdout);

    clock_t start = clock();
    
    cin >> n >> m;
    adj.resize(n);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        u--; v--; // Convert to 0-based indexing
        adj[u].push_back({v, i});
        adj[v].push_back({u, i});
    }
    
    findBridgesAndArticulationPoints();
    
    cout << (double)(clock() - start) / CLOCKS_PER_SEC << endl;  
    
    cout << bridgeCnt << " " << articulationPointsCnt << "\n";
    for (int i = 0; i < m; i++) {
        if (isBridge[i]) cout << i + 1 << " ";
    }
    cout << "\n";
    for (int i = 0; i < n; i++) {
        if (isArticulationPoint[i]) cout << i + 1 << " ";
    }
    cout << "\n";
    
    return 0;
}