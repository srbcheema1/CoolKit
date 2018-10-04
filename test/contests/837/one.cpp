#include<bits/stdc++.h>
#define dout if(debug) cout<<" "

using namespace std;

int debug = 1;

typedef unsigned long long int ulli;
typedef unsigned int ui;
typedef pair<int,int> mp;
typedef vector<vector<int> > matrix;

const int mod = 1e9+7;

bool is_big(char a){
    if (a >= 'A' and a <= 'Z') return true; return false;
}

void solve(){
    int n;
    cin>>n;
    string str;
    getline(cin,str);
    getline(cin,str);
    int maxx = 0,now = 0;
    for(int i=0;i< (int)str.length();i++){
        //cout << str[i] << endl;
        if(str[i] == 32){
            maxx = max(maxx , now);
            now = 0;
        }
        if(is_big(str[i])){
            now ++;
        }
    }
    maxx = max(maxx,now);
    cout << maxx << endl;
}

signed main(){
    ios_base::sync_with_stdio(0);cin.tie(0);
    int t=1;
    //cin>>t;
    while(t--)solve();
}
