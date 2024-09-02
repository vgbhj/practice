#include <bits/stdc++.h>

using namespace std;

class Solution {
public:
    int numberOfSubarrays(vector<int>& nums, int k) {
        vector<int> pref(nums.size());
        int ans = 0;
        int now_odd = 0;
        pref[0]++;
        for(int i = 0; i < nums.size(); ++i){
            now_odd += nums[i] & 1;
            if(now_odd-k >= 0){
                ans += pref[now_odd-k];
            }
            pref[now_odd]++;
        }

        return ans;
    }
};

int main(){
    Solution solv;
    vector<int> v = {1,1,2,1,1};
    cout << solv.numberOfSubarrays(v, 3);
    return 0;
}