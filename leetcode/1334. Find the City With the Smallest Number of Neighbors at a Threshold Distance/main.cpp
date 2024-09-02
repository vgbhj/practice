#include <bits/stdc++.h>

using namespace std;

class Solution {
public:
    int findTheCity(int n, vector<vector<int>>& edges, int distanceThreshold) {
        vector<vector<pair<int,int>>> g(n);
        for(auto _ : edges){
            g[_[0]].push_back({_[1], _[2]});
            g[_[1]].push_back({_[0], _[2]});
        }
        int mn = 999999;
        int ans = 0;
        for(int i = 0; i < n; ++i){
            int a = dijkstra(i, n, g, distanceThreshold);
            if(a <= mn){
                ans = i;
                mn = a;
            } 
        }

        return ans;
    }

    int dijkstra(int s, int n, vector<vector<pair<int,int>>>& g, int distanceThreshold) {
        const int maxn = 1e5, inf = 1e9;
        int count = 0;
        vector<int> d(n, inf), a(n, 0);
        d[s] = 0;
        for (int i = 0; i < n; i++) {
            // находим вершину с минимальным d[v] из ещё не помеченных
            int v = -1;
            for (int u = 0; u < n; u++)
                if (!a[u] && (v == -1 || d[u] < d[v]))
                    v = u;
            // помечаем её и проводим релаксации вдоль всех исходящих ребер
            a[v] = true;
            for (auto [u, w] : g[v])
                d[u] = min(d[u], d[v] + w);
        }
        for(int i = 0; i < n; ++i){
            if(i != s){
                if(d[i] <= distanceThreshold){
                    count++;
                }
            }
        }
        return count;
}
};
int main(){
    Solution solv;
    int n = 5;
    vector<vector<int>> edges = {{0,1,2},{0,4,8},{1,2,3},{1,4,2},{2,3,1},{3,4,1}};
    int distanceThreshold = 2;
    cout << solv.findTheCity(n, edges, distanceThreshold);
    return 0;
}