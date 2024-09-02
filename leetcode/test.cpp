#include <bits/stdc++.h>

using namespace std;

class Solution {
};

int main(){
    vector<int> v = {1, 2, 3};
    cout << *(v.begin() + v.size()/2 - 1) << endl;
    cout << *(v.begin() + v.size()/2 + 1);
    vector<int> v1 = vector<int>(v.end(), v.end());
    cout << v1.size();
    return 0;
}