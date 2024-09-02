#include <bits/stdc++.h>

using namespace std;

class Solution {
public:
    int maxDistance(vector<int>& position, int m) {
        sort(position.begin(), position.end());
        int left, right; // left -> right
        left = 1;
        right = 1e9;
        int mid = 0;
        while(left < right){
            mid = (left + right + 1) / 2;
            int tmp_p = position[0];
            int count = 1;
            for(int i = 1; i < position.size(); ++i){
                if(position[i]-tmp_p >= mid){
                    count++;
                    tmp_p = position[i];
                }
            }

            if(count >= m){
                left = mid;
            }
            else{
                right = mid - 1;
            }

        }

        return left;
    }
};

int main(){
    Solution solv;
    vector<int> v = {5,4,3,2,1,1000000000};
    cout << solv.maxDistance(v, 2);
    return 0;
}