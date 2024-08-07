#include <bits/stdc++.h>

using namespace std;

class Solution {
public:
    long long minimumCost(string source, string target, vector<char>& original, vector<char>& changed, vector<int>& cost) {
        long long sm = 0;
        int n = cost.size();
        vector<pair<pair<char, char>, int>> v(n);
        for(int i = 0; i < n; ++i){
            v[i] = {{original[i], changed[i]}, cost[i]};
        }

        sort(v.begin(), v.end(),
            [] (const auto& lhs, const auto& rhs) {
                return lhs.second < rhs.second;
        });

        for(int i = 0; i < source.size(); ++i){
            char find_source = source[i];
            char find_target = target[i];
            if(find_source == find_target){
                continue;
            }

            char tmp_source;
            char tmp_target;
            bool flag = true;

            for(int j = 0; j < n; ++j){
                tmp_source = v[j].first.first;
                tmp_target = v[j].first.second;

                // Debug
                // cout << find_source << ' ' << find_target << ' ' << tmp_source << ' ' << tmp_target << '\n';
                

                if(tmp_source == find_source && tmp_target == find_target){
                     // Debug
                cout << find_source << ' ' << find_target << ' ' << tmp_source << ' ' << tmp_target << '\n';
                cout << v[j].second << "===\n";
                    sm += v[j].second;
                    flag = false;
                }
            }
            if(flag){
                return -1;
            }
        }

        return sm;
    }
};


int main(){
    Solution solv;
    string source = "abcd";
    string target = "acbe";
    vector<char> original = {'a','b','c','c','e','d'}; 
    vector<char> changed = {'b','c','b','e','b','e'};
    vector<int> cost = {2,5,5,1,2,20};
    cout << solv.minimumCost(source, target, original, changed, cost);
    return 0;
}