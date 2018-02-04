#include <bits/stdc++.h>

using namespace std;

const int mod = 1e9 + 7;
const int N = 1e5 + 2;

int _add(int x, int y) {
    int res = (x + y) % mod;
    return res < 0 ? res + mod : res;
}

int mul(int x, int y) {
    int res = (x * 1LL * y) % mod;
    return res < 0 ? res + mod : res;
}

#define ii pair<int,int>

int n;
int ans = 0;
int a[N];
map<ii, int> lh, hl;

map<ii, int>::iterator findlh(int v) {
    auto it = lh.lower_bound({v, 0});
    return (it->first.first == v) ? it : lh.end();
}

map<ii, int>::iterator findhl(int v) {
    auto it = hl.lower_bound({v, 0});
    return (it->first.first == v) ? it : hl.end();
}

map<ii, int>::iterator toomuch(int v) {
    auto it=hl.lower_bound({v,0});
    if(it->first.first==v) it=prev(it);
    return lh.find({it->first.second,it->first.first});
}

void add(int v) {
    if (findlh(v) != lh.end()) {
        auto it = findlh(v);
        auto itt = hl.find(ii{it->first.second, it->first.first});
        if (findhl(v) != hl.end()) {
            auto itt2 = findhl(v);
            auto it2 = lh.find(ii{itt2->first.second, itt2->first.first});
            if ((it2->first.second - itt2->first.second) > 1) {
                lh[{itt2->first.second, it->first.second}]++;
                hl[{it->first.second, itt2->first.second}]++;
                ans++;
            }
            ans--;
            it2->second--;
            itt2->second--;
            if (it2->second == 0) lh.erase(it2);
            if (itt2->second == 0) hl.erase(itt2);
        } else {
            if ((it->first.second - (v - 1)) > 1) {
                lh[{v - 1, it->first.second}]++;
                hl[{it->first.second, v - 1}]++;
                ans++;
            }
        }
        ans--;
        it->second--;
        itt->second--;
        if (it->second == 0) lh.erase(it);
        if (itt->second == 0) hl.erase(itt);
    } else if (findhl(v) != hl.end()) {
        auto itt = findhl(v);
        auto it = lh.find(ii{itt->first.second, itt->first.first});
        if (findlh(v) != lh.end()) {
            auto it2 = findlh(v);
            auto itt2 = hl.find(ii{it2->first.second, it2->first.first});
            if ((it2->first.first - itt->first.second) > 1) {
                ans++;
                lh[ii{itt->first.second, it2->first.first}]++;
                hl[ii{it2->first.first, itt->first.second}]++;
            }
            ans--;
            it2->second--;
            itt2->second--;
            if (it2->second == 0) lh.erase(it2);
            if (itt2->second == 0) hl.erase(itt2);
        } else {
            if ((v + 1 - itt->first.second) > 1) {
                hl[{v + 1, itt->first.second}]++;
                lh[{itt->first.second, v + 1}]++;
                ans++;
            }
        }
        ans--;
        it->second--;
        itt->second--;
        if (it->second == 0) lh.erase(it);
        if (itt->second == 0) hl.erase(itt);
    } else {
        lh[{v - 1, v + 1}]++;
        hl[{v + 1, v - 1}]++;
        ans++;
    }
}

void del(int v) {
    if (findlh(v - 1) != lh.end()) {
        auto it = findlh(v - 1);
        auto itt = hl.find({it->first.second, it->first.first});
        if (findhl(v + 1) != hl.end()) {
            auto itt2 = findhl(v + 1);
            auto it2 = lh.find({itt2->first.second, itt2->first.first});
            if (it->first.second - itt2->first.second > 1) {
                lh[{itt2->first.second, it->first.second}]++;
                hl[{it->first.second, itt2->first.second}]++;
                ans++;
            }
            ans--;
            it2->second--;
            itt2->second--;
            if (it2->second == 0) lh.erase(it2);
            if (itt2->second == 0) hl.erase(itt2);
        }
        else {
            if (it->first.second - v > 1) {
                lh[{v, it->first.second}]++;
                hl[{it->first.second, v}]++;
                ans++;
            }
        }
        it->second--;
        itt->second--;
        ans--;
        if (it->second == 0) lh.erase(it);
        if (itt->second == 0) hl.erase(itt);
    }
    else if (findhl(v + 1) != hl.end()) {
        auto itt = findhl(v + 1);
        auto it = lh.find({itt->first.second, itt->first.first});
        if (findlh(v-1) != lh.end()) {
            auto it2 = findlh(v-1);
            auto itt2 = hl.find({it2->first.second, it2->first.first});
            if ((it2->first.first - itt->first.second) > 1) {
                lh[{itt->first.second, it2->first.first}]++;
                hl[{it2->first.first, itt->first.second}]++;
                ans++;
            }
            ans--;
            it2->second--;
            itt2->second--;
            if (it2->second == 0) lh.erase(it2);
            if (itt2->second == 0) hl.erase(itt2);
        }
        else {
            if ((v - itt->first.second) > 1) {
                hl[{v, itt->first.second}]++;
                lh[{itt->first.second, v}]++;
                ans++;
            }
        }
        ans--;
        it->second--;
        itt->second--;
        if (it->second == 0) lh.erase(it);
        if (itt->second == 0) hl.erase(itt);
    }
    else {
        auto it = toomuch(v);
        auto itt = hl.find({it->first.second, it->first.first});
        ii now = {it->first.first, v}, cur = {v, it->first.second};
        bool isnow = 1, iscur = 1;
        if (findlh(v - 1) != lh.end()) {
            auto it2 = findlh(v - 1);
            auto itt2 = hl.find({it2->first.second, it2->first.first});
            if ((it2->first.first - now.first) > 1) {
                lh[{now.first, it2->first.first}]++;
                hl[{it2->first.first, now.first}]++;
                ans++;
            }
            ans--;
            it2->second--;
            itt2->second--;
            if (it2->second == 0) lh.erase(it2);
            if (itt2->second == 0) hl.erase(itt2);
            isnow = 0;
        }
        if (findhl(v + 1) != hl.end()) {
            auto itt2 = findhl(v + 1);
            auto it2 = lh.find({itt2->first.second, itt2->first.first});
            if ((cur.second - itt2->first.second) > 1) {
                lh[{itt2->first.second, cur.second}]++;
                hl[{cur.second, itt2->first.second}]++;
                ans++;
            }
            ans--;
            it2->second--;
            itt2->second--;
            if (it2->second == 0) lh.erase(it2);
            if (itt2->second == 0) hl.erase(itt2);
            iscur = 0;
        }
        if (isnow) {
            if (now.second - now.first > 1) {
                ans++;
                lh[(now)]++;
                hl[{now.second, now.first}]++;
            }
        }
        if (iscur) {
            if ((cur.second - cur.first) > 1) {
                ans++;
                lh[(cur)]++, hl[{cur.second, cur.first}]++;
            }
        }
        ans--;
        it->second--;
        itt->second--;
        if (it->second == 0) lh.erase(it);
        if (itt->second == 0) hl.erase(itt);
    }
}


signed main() {
    int q;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> a[i];
        add(a[i]);
    }
    //cout << ans << "\n";
    int print = 0;
    cin >> q;
    for (int i = 1; i <= q; i++) {
        int id, val;
        cin >> id >> val;
        del(a[--id]);
        add(val);
        a[id] = val;
      //  cout << ans << "\n";
        print = _add(print, mul(ans, i));
    }
    cout << print;
}
