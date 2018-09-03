import requests
from sys import argv
from bs4 import BeautifulSoup
import pandas as pd

def user_contests(name):
    req=requests.get('http://codeforces.com/contests/with/'+name)
    soup=BeautifulSoup(req.text,'html.parser')

    a=soup.find_all(id='body')
    b=a[0].find_all('div',recursive=False)
    #inside body
    c=b[3].find_all('div',recursive=False)
    d=c[1].find_all('div',recursive=False)
    e=d[2].find_all('div',recursive=False)
    f=e[5].find_all('table',recursive=False)
    g=f[0].find_all('thead',recursive=False)
    #went inside table
    h=g[0].find_all('tr',recursive=False)
    #went inside thead
    l=h[0].get_text('')
    i=f[0].find_all('tbody',recursive=False)
    j=i[0].find_all('tr',recursive=False)
    #print(j[0].get_text())

    a=[],b=[],c=[],d=[]
    for row in i[0].findAll('tr'):
        cells = row.findAll('td')
        states=row.findAll('a') #To store second column data
        if len(cells)>=1: #Only extract table body not heading
            a.append(cells[0].find(text=True).strip())
            if(len(states[0].find(text=True))==52):
                b.append("CF Round : "+states[0].find(text=True)[20:23])
            else:
                b.append("EC Round : "+states[0].find(text=True)[30:33])
            c.append(states[1].find(text=True).strip().strip('\r\n').strip())
            d.append(states[2].find(text=True).lstrip('\n').strip('\r').strip('\n').strip())

    df=pd.DataFrame(b,columns=['Contest  '])
    df['Rank']=c
    df[' Solved']=d
    return df


if(__name__=="__main__"):
    name='srbcheema1'
    if(len(argv)==2):
        name=argv[1]

    df = user_contests(name)
    print(df)
