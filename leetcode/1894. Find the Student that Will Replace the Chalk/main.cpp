#include <bits/stdc++.h>

using namespace std;

class Solution {
public:
    int chalkReplacer(vector<int> chalk, int k) {
        int i = 0;
        long long sum = 0;
        for_each(chalk.begin(), chalk.end(), [&](int i) {
            sum += i;
        });
        while (k > sum)
        {
            k -= sum;
        }
        
        while(k > 0){
            k -= chalk[i];
            if(k < 0){
                return i;
            }
            // Deubug
            // cout << k << ' ' << chalk[i] << '\n'; 
            
            i++;
            i %= chalk.size();
        }

        return i;
    }
};


int main(){
    Solution solv;
    cout << solv.chalkReplacer({3,4,1,2}, 25);
    return 0;
}