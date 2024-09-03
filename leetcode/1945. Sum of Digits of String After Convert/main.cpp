#include <bits/stdc++.h>

using namespace std;

class Solution {
public:
    int getLucky(string s, int k) {
        int ans = 0;
        string tmp = "";

        for(auto _ : s){
            tmp += to_string(_ - 96);
        }

        for(int i = 0; i < k; ++i){
            ans = 0;
            for(auto _ : tmp){
                ans += _ - '0';
            }
            tmp = to_string(ans);
        }

        return ans;
    }
};

int main(){
    Solution solv;
    cout << solv.getLucky("iiii", 1);
    return 0;
}