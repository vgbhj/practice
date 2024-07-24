#include <bits/stdc++.h>

using namespace std;

class Solution {
public:

    vector<int> sortJumbled(vector<int>& mapping, vector<int>& nums) {
        
        sort(nums.begin(), nums.end(), [&mapping] (int n1, int n2) {
        // cout << "==" << n1 << ' ' << n2 << "==\n";
        int tmp_1, tmp_2;
        tmp_1 = tmp_2 = 0;
        int i = 1;
            do{
                tmp_1 += mapping[n1%10] * i;
                // cout << n1 << ' ' << n1%10 << "---\n";
                n1 /= 10;
                i *= 10;
            }while(n1);
        i = 1;
            do{
                tmp_2 += mapping[n2%10] * i;
                
                n2 /= 10;
                i *= 10;
            }while(n2);
            // cout << tmp_1 << ' ' << tmp_2 << ' ' << (tmp_1 < tmp_2) << '\n';
            return tmp_1 < tmp_2;
    });

        return nums;
    }
};

int main(){
    Solution solv;
    vector<int> mapping = {9,8,7,6,5,4,3,2,1,0};
    vector<int> nums = {0,1,2,3,4,5,6,7,8,9};
    vector<int> ans = solv.sortJumbled(mapping, nums);
    cout << mapping[0];
    cout << 0%10;
    cout << mapping[0%10];
    for(auto _ : ans){
        cout << _ << ' ';
    }
    cout << "====\n";
    sort(nums.begin(), nums.end(), greater<int>());
    for(auto _ : nums){
        cout << _ << ' ';
    }
    return 0;
}