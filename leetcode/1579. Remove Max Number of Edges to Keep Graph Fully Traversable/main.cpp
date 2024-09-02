#include <bits/stdc++.h>

using namespace std;

class Solution {    
public:
    int maxNumEdgesToRemove(int n, vector<vector<int>>& edges) {
        int ans = 0;
        int edgeCountA = 0;
        int edgeCountB = 0;
        vector<int> sizeA(n+1, 1);
        vector<int> sizeB(n+1, 1);
        vector<int> representativeA(n+1);
        vector<int> representativeB(n+1);

        for(int i = 1; i < n+1; ++i){
            representativeA[i] = i;
            representativeB[i] = i;
        }

        vector<vector<int>> graphA(n+1);
        vector<vector<int>> graphB(n+1);

        for(const auto& edge: edges){
            if(edge[0] == 3){
                bool isPlusAns = false;
                // graphA check
                if(find(edge[1], representativeA) != find(edge[2], representativeA) ){
                    combine(edge[1], edge[2], representativeA, sizeA);
                    
                    edgeCountA++;
                }
                else{
                    isPlusAns = true;
                }

                // graphB check
                if(find(edge[1], representativeB) != find(edge[2], representativeB)){
                    combine(edge[1], edge[2], representativeB, sizeB);
                    
                    edgeCountB++;
                }
                else{
                    isPlusAns = true;
                }

                if(isPlusAns){
                    ans++;
                }
            }
        }

        // Alice
        for(const auto& edge: edges){
            if(edge[0] == 1){
                if(find(edge[1], representativeA) != find(edge[2], representativeA)){
                    combine(edge[1], edge[2], representativeA, sizeA);
                    
                    edgeCountA++;
                }
                else{
                    ans++;
                }
            }
        }

        // Bob
        for(const auto& edge: edges){
            if(edge[0] == 2){
                if(find(edge[1], representativeB) != find(edge[2], representativeB)){
                    combine(edge[1], edge[2], representativeB, sizeB);
                    
                    edgeCountB++;
                }
                else{
                    ans++;
                }
            }
        }

        // Debug
        // cout << edgeCountA << ' ' << edgeCountB << '\n';
        if(edgeCountA < n-1) return -1;
        if(edgeCountB < n-1) return -1;
        
        return ans;
    }

    int find(int u, vector<int>& representative)
    {
    if(u == representative[u])
        return u;
    
    else
        return representative[u] = find(representative[u], representative);
    }

    bool combine (int u, int v, vector<int>& representative, vector<int>& size)
    {
        u = find(u, representative);
        v = find(v, representative);
        
        if(u == v)
            return false;
        
        else
        {
            if(size[u] > size[v])
            {
                representative[v] = u;
                size[u] += size[v];
            }
            
            else
            {
                representative[u] = v;
                size[v] += size[u];
            }
        
        }
        return true;
    }

};


int main(){
    Solution solv;
    int n = 4;
    // case 1
    // vector<vector<int>> v = {{3,1,2},{3,2,3},{1,1,3},{1,2,4},{1,1,2},{2,3,4}};
    // ans = 2

    // case 3
    // vector<vector<int>> v = {{3,2,3},{1,1,2},{2,3,4}};
    // abs = -1 

    // case 20
    
    // vector<vector<int>> v = {{3,1,2}, {3,3,4}, {1,1,3},{2,2,4}};

    // case 18
    n = 13;
    vector<vector<int>> v = {{1,1,2},{2,1,3},{3,2,4},{3,2,5},{1,2,6},{3,6,7},{3,7,8},{3,6,9},{3,4,10},{2,3,11},{1,5,12},{3,3,13},{2,1,10},{2,6,11},{3,5,13},{1,9,12},{1,6,8},{3,6,13},{2,1,4},{1,1,13},{2,9,10},{2,1,6},{2,10,13},{2,2,9},{3,4,12},{2,4,7},{1,1,10},{1,3,7},{1,7,11},{3,3,12},{2,4,8},{3,8,9},{1,9,13},{2,4,10},{1,6,9},{3,10,13},{1,7,10},{1,1,11},{2,4,9},{3,5,11},{3,2,6},{2,1,5},{2,5,11},{2,1,7},{2,3,8},{2,8,9},{3,4,13},{3,3,8},{3,3,11},{2,9,11},{3,1,8},{2,1,8},{3,8,13},{2,10,11},{3,1,5},{1,10,11},{1,7,12},{2,3,5},{3,1,13},{2,4,11},{2,3,9},{2,6,9},{2,1,13},{3,1,12},{2,7,8},{2,5,6},{3,1,9},{1,5,10},{3,2,13},{2,3,6},{2,2,10},{3,4,11},{1,4,13},{3,5,10},{1,4,10},{1,1,8},{3,3,4},{2,4,6},{2,7,11},{2,7,10},{2,3,12},{3,7,11},{3,9,10},{2,11,13},{1,1,12},{2,10,12},{1,7,13},{1,4,11},{2,4,5},{1,3,10},{2,12,13},{3,3,10},{1,6,12},{3,6,10},{1,3,4},{2,7,9},{1,3,11},{2,2,8},{1,2,8},{1,11,13},{1,2,13},{2,2,6},{1,4,6},{1,6,11},{3,1,2},{1,1,3},{2,11,12},{3,2,11},{1,9,10},{2,6,12},{3,1,7},{1,4,9},{1,10,12},{2,6,13},{2,2,12},{2,1,11},{2,5,9},{1,3,8},{1,7,8},{1,2,12},{1,5,11},{2,7,12},{3,1,11},{3,9,12},{3,2,9},{3,10,11}};

    // ans = 114
    cout << solv.maxNumEdgesToRemove(n, v);
    return 0;
}