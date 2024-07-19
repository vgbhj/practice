#include <bits/stdc++.h>

using namespace std;

class Solution {
public:
    vector<int> luckyNumbers (vector<vector<int>>& matrix) {
        vector<int> ans;
        map<int, int> mp;
        // for in every row
        for(int i = 0; i < matrix.size(); ++i){
            int mn = 10e6;
            // for in row
            for(int j = 0; j < matrix[i].size(); ++j){
                if(matrix[i][j] < mn) mn = matrix[i][j];
            }
            if(mn != 10e6) mp[mn]++;
        }
        // for in every column index
        for(int i = 0; i < 50; ++i){
            int mx = 0;
            // for in every column by index
            for(int j = 0; j < matrix.size(); ++j){
                if(matrix[j].size() > i){
                    if(matrix[j][i] > mx) mx = matrix[j][i];
                }
            }
            if(mx != 0) mp[mx]++;
        }

        for(auto _ : mp){
            if(_.second == 2){
                ans.push_back(_.first);
            }
        }
        return ans;
    }
};

int main(){
    Solution solv;
    return 0;
}