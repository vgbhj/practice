#include <bits/stdc++.h>

using namespace std;

class Solution {
public:
    vector<vector<int>> restoreMatrix(vector<int>& rowSum, vector<int>& colSum) {
        vector<vector<int>> ans(
            rowSum.size(),
            std::vector<int>(colSum.size()));
        // 
        for(int i = 0; i < rowSum.size(); ++i){
            for(int j = 0; j < colSum.size(); ++j){
                if(rowSum[i] < colSum[j]){
                     ans[i][j] = rowSum[i];
                     colSum[j] -= rowSum[i];
                     rowSum[i] -= rowSum[i];
                }
                else if(rowSum[i] == colSum[j]){
                    ans[i][j] = rowSum[i];
                    rowSum[i] = 0;
                    colSum[j] = 0;

                }
                else{ // rowSum[i] > colSum[j]
                    ans[i][j] = colSum[j];
                    rowSum[i] -= colSum[j];
                    colSum[j] -= colSum[j];
                }
            }
        }

        return ans;

    }
};

int main(){
    Solution solv;
    return 0;
}