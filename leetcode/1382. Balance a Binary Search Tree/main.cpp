#include <bits/stdc++.h>

using namespace std;


struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

class Solution {
public:
    TreeNode* balanceBST(TreeNode* root) {
        vector<int> sort_arr; 
        getArr(root, sort_arr);
        sort(sort_arr.begin(), sort_arr.end());
        // for(auto _ : sort_arr){
        //     cout << _ << ' ';
        // }
        // cout << "=====\n";
        return buildBalancedBST(sort_arr);
    }
private:
    void getArr(TreeNode* root, vector<int>& v){
        if(!root){
            return;
        }
        v.push_back(root->val);
        getArr(root->left, v);
        getArr(root->right, v);
    }

    TreeNode* buildBalancedBST(vector<int>& v){
        if(v.size() == 0){
            return nullptr;
        }
        int mid = v.size() / 2;
        TreeNode* root = new TreeNode(v[mid]);
        if(v.size() < 2){
            return root;
        }
        vector<int> v_left = vector<int>(v.begin(), v.begin() + mid);
        vector<int> v_right = vector<int>(v.begin() + mid + 1, v.end());
        root->left = buildBalancedBST(v_left);
        root->right = buildBalancedBST(v_right);
        return root;
    }

};

int main(){
    TreeNode* t = new TreeNode(1);
    t->right = new TreeNode(2);
    t->right->right = new TreeNode(3);
    t->right->right->right = new TreeNode(4);
    Solution solv;
    TreeNode* t2 = solv.balanceBST(t);
    return 0;
}