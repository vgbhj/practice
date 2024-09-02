#include <bits/stdc++.h>

using namespace std;

class Solution {
public:
    vector<vector<int>> getAncestors(int n, vector<vector<int>>& edges) {
        vector<vector<int>> ans(n);
        vector<vector<int>> graph(n);

        for(const auto& edge: edges){
            graph[edge[0]].push_back(edge[1]);
        }

        for(int i = 0; i < n; ++i){
            vector<bool> visit(n, false);
            dfs(graph, i, i, ans, visit);
        }

        for (int i = 0; i < n; ++i) {
            sort(ans[i].begin(), ans[i].end());
        }

        return ans;
    }

private:
    void dfs(vector<vector<int>>& graph, int parent, int curr, vector<vector<int>>& ans, vector<bool>& visit){
        visit[curr] = true;
        for(auto _ : graph[curr]){
            if(!visit[_]){
                ans[_].push_back(parent);
                dfs(graph, parent, _, ans, visit);
            }
        }
    }
};

int main(){
    Solution solv;
    int n = 8;
    vector<vector<int>> v = {{0,3},{0,4},{1,3},{2,4},{2,7},{3,5},{3,6},{3,7},{4,6}};
    vector<vector<int>> ans = solv.getAncestors(n, v);
    for(auto _ : ans){
            for(auto __ : _){
                cout << __ << "; ";
            }
            cout << '\n';
        }
    return 0;
}