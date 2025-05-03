#include "testlib.h"

#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1e6;
const int MAXM = 2e6;

int main(int argc, char* argv[]) {
    registerGen(argc, argv, 1);
    prepareOpts(argc, argv);

    ios_base::sync_with_stdio(0);
    cin.tie(0);cout.tie(0);
    
    freopen("S.INP", "w", stdout);

    int n = 2000;
    bool sparse = true;

    int m;
    if(sparse) {
        m = rnd.next(2.0 * n, 2.5 * n);
    } else {
        long long max_edges = n * (n - 1) / 2;
        assert(max_edges <= 1'000'000'000);
        m = rnd.next(0.9 * max_edges, 1.0 * max_edges);
    }

    assert(1 <= n && n <= MAXN);
    assert(n - 1 <= m && m <= MAXM);

    vector<pair<int, int>> edges;
    set<pair<int, int>> edgeSet;

    for (int i = 2; i <= n; ++i) {
        int parent = rnd.next(1, i - 1);
        edges.emplace_back(parent, i);
        edgeSet.insert({min(parent, i), max(parent, i)});
    }

    int extraEdges = m - (n - 1);

    if (n > 2000) {
        while (extraEdges--) {
            int u, v;
            do {
                u = rnd.next(1, n);
                v = rnd.next(1, n);
            } while (u == v || edgeSet.count({min(u, v), max(u, v)}));
            edges.emplace_back(u, v);
            edgeSet.insert({min(u, v), max(u, v)});
        }
    } else {
        vector<pair<int, int>> allPairs;
        for (int u = 1; u <= n; ++u) {
            for (int v = u + 1; v <= n; ++v) {
                if (!edgeSet.count({u, v}))
                    allPairs.emplace_back(u, v);
            }
        }
        shuffle(allPairs.begin(), allPairs.end());
        for (int i = 0; i < extraEdges && i < int(allPairs.size()); ++i) {
            edges.push_back(allPairs[i]);
        }
    }

    vector<int> p(n + 1);
    for (int i = 1; i <= n; ++i) p[i] = i;
    shuffle(p.begin() + 1, p.end());

    println(n, m);
    for (pair<int, int> edge : edges) {
        println(p[edge.first], p[edge.second]);
    }

    return 0;
}
