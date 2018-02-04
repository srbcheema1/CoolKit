#include<bits/stdc++.h>
#define dout if(debug) cout<<" "

typedef long long int lli;
const lli inf = 1e14;
const lli mod = 1e9+7;

using namespace std;
lli debug = 0;

signed main(){
    lli n;
    cin>>n;
    vector<lli> arr(n+1);

    map<lli,lli> mapp;
    map<lli,lli> temp;
    for(lli i=1;i<n+1;i++){
        cin>>arr[i];
        mapp[arr[i]]++;
        temp[arr[i]]++;
    }

    lli last=temp.begin()->first-1;
    lli fa = 0;
    dout<<temp.size()<<endl;
    while(temp.size()){
        set<lli> sett;
        lli minn = inf;
        for(auto p : temp){
            if(p.first > last+1){
                //process all till now
                break;
            }
            minn = min(p.second,minn);
            sett.insert(p.first);
            last = p.first;
        }
        for(auto p : sett){
            temp[p]-=minn;
            if(temp[p]==0)temp.erase(p);
        }
        fa+=minn;
        last=temp.begin()->first-1;
    }


    lli q;
    lli ans = 0;
    cin>>q;
    for(lli i = 1 ; i<=q;i++){
        lli id,val,l,r;
        cin>>id>>val;
        if(arr[id]==val){
            ans = (ans + (i*fa)%mod)%mod;
            dout<<i<<" "<<fa<<" "<<ans<<endl;
            continue;
        }

        lli a = arr[id];//old num
        lli b = val;//new num

        lli aa = mapp[arr[id]],bb;//freq of old val



        //remove old
        if(mapp.find(a-1)==mapp.end()) l = 0;
        else l = mapp[a-1];
        if(mapp.find(a+1)==mapp.end()) r = 0;
        else r = mapp[a+1];

        dout<<"l="<<l<<" r="<<r<<" a="<<a<<endl;
        dout<<"l="<<l<<" r="<<r<<" aa="<<aa<<endl;

        if(l==aa and r>=aa){fa++;dout<<1<<endl;}
        else if (r==aa and l>=aa){fa++;dout<<2<<endl;}
        else if (aa>l and aa>r){fa--;dout<<3<<endl;}
        else if (aa<l and aa<r)fa++;
//        fa = (fa+mod)%mod;

        mapp[arr[id]]--;
        if(mapp[arr[id]]==0)mapp.erase(arr[id]);
        if(mapp.find(val)==mapp.end())bb=0;
        else bb = mapp[val];//freq of new val //may need attention


        //add new
        if(mapp.find(b-1)==mapp.end()) l = 0;
        else l = mapp[b-1];
        if(mapp.find(b+1)==mapp.end()) r = 0;
        else r = mapp[b+1];

        dout<<"l="<<l<<" r="<<r<<" b="<<b<<endl;
        dout<<"l="<<l<<" r="<<r<<" bb="<<bb<<endl;

        if(l==bb and r<=bb){fa++;dout<<4<<endl;}
        else if (r==bb and l<=bb){fa++;dout<<5<<endl;}
        else if (bb<l and bb<r){fa--;dout<<6<<endl;}
        else if(bb>l and bb>r){fa++;dout<<7<<endl;}
//        fa = (fa+mod)%mod;

        arr[id]=val;
        mapp[arr[id]]++;



        //ans cALC
        ans = (ans + (i*fa)%mod)%mod;
        dout<<i<<" "<<fa<<" "<<ans<<endl;

    }
    cout<<ans;
}
