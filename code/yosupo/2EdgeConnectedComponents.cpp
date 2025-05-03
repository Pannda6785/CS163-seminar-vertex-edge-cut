#include <bits/stdc++.h>

using namespace std;

int n, m;
int timeDfs;
vector<vector<int>> adj;
vector<int> low, num;
vector<vector<int>> coms;
stack<int> st;

void tarjan(int u, int parent) {
    st.push(u);
    bool mul = false;
    low[u] = num[u] = ++timeDfs;

    for (int v : adj[u]) {
        if (num[v] != -1) {
            if(v != parent || mul) low[u] = min(low[u], num[v]);
            else mul = true;
            continue;
        }
        
        tarjan(v, u);
        low[u] = min(low[u], low[v]);
    }

    if (low[u] == num[u]) {
        vector<int> com;
        while (true) {
            int v = st.top(); st.pop();
            com.push_back(v);
            if (v == u) break;
        }
        coms.push_back(com);
    }
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);

    cin >> n >> m;

    adj.resize(n);
    low.resize(n, 0);
    num.resize(n, -1);

    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    for (int i = 0; i < n; i++) {
        if (num[i] == -1) tarjan(i, -1);
    }

    cout << coms.size() << "\n";
    for (const vector<int>& com : coms) {
        cout << com.size() << " ";
        for (int v : com) cout << v << " ";
        cout << "\n";
    }

}