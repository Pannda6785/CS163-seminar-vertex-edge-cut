#include <iostream>
#include <vector>
#include <ctime>
#include <algorithm>

using namespace std;

// DFS to mark reachable vertices, skipping forbidden vertices and ignored edges
void DFS(int u, const vector<vector<int>>& adj, vector<bool>& visited,
         const vector<bool>& forbidden, pair<int,int> ignore_edge) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!forbidden[v] && !visited[v]) {
            // Check if edge (u, v) is the one to ignore
            if (ignore_edge.first != -1) {
                int min_uv = min(u, v);
                int max_uv = max(u, v);
                if (min_uv == ignore_edge.first && max_uv == ignore_edge.second) {
                    continue; // Skip this edge
                }
            }
            DFS(v, adj, visited, forbidden, ignore_edge);
        }
    }
}

// Count connected components, considering forbidden vertices and ignored edges
int count_components(const vector<vector<int>>& adj, const vector<bool>& forbidden,
                    pair<int,int> ignore_edge) {
    int n = adj.size();
    vector<bool> visited(n, false);
    int components = 0;
    for (int i = 0; i < n; i++) {
        if (!forbidden[i] && !visited[i]) {
            DFS(i, adj, visited, forbidden, ignore_edge);
            components++;
        }
    }
    return components;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
    
    freopen("S.INP", "r", stdin);
    freopen("S.OUT", "w", stdout);

    clock_t start = clock();

    int n, m;
    cin >> n >> m;

    vector<vector<int>> adj(n);
    vector<pair<int,int>> edges(m);

    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        u--, v--;
        adj[u].push_back(v);
        adj[v].push_back(u);
        edges[i] = {min(u, v), max(u, v)}; // Store edge with smaller index first
    }

    // Original number of components
    int k = count_components(adj, vector<bool>(n, false), {-1, -1});

    // Find bridges
    vector<int> bridges;
    for (int i = 0; i < m; i++) {
        pair<int,int> e = edges[i];
        int comp = count_components(adj, vector<bool>(n, false), e);
        if (comp > k) {
            bridges.push_back(i + 1); // 1-based index
        }
    }

    // Find articulation points
    vector<int> articulationPoints;
    for (int i = 0; i < n; i++) {
        vector<bool> forbidden(n, false);
        forbidden[i] = true;
        int comp = count_components(adj, forbidden, {-1, -1});
        if (comp > k) {
            articulationPoints.push_back(i + 1); // 1-based index
        }
    }

    cout << (double)(clock() - start) / CLOCKS_PER_SEC << endl;  

    // Output results
    cout << bridges.size() << " " << articulationPoints.size() << endl;

    sort(bridges.begin(), bridges.end());
    sort(articulationPoints.begin(), articulationPoints.end());
    
    for (int i = 0; i < (int) bridges.size(); i++) {
        cout << bridges[i] << " ";
    }
    cout << endl;
    for (int i = 0; i < (int) articulationPoints.size(); i++) {
        cout << articulationPoints[i] << " ";
    }
    cout << endl;

    return 0;
}