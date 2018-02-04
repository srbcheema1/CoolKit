import requests
import bs4
from sys import argv


def display_problems(contest_num=920):
    contest_num = str(contest_num)

    req=requests.get("http://codeforces.com/contest/920")
    soup = bs4.BeautifulSoup(req.text,"html.parser")
    a = soup.find_all(id='body')
    b = a[0].find_all('div',recursive=False)
    c = b[3].find_all('div',recursive=False)
    d = c[1].find_all('div',recursive=False)
    e = d[1].find_all('div',recursive=False)
    f = e[5].find_all('table',recursive=False)
#entering table
    g=f[0].find_all('tr')
    l=len(g)

    maxx=0
    for i in range(1,l):
     a=chr(64+i)        #alphabet
     row = g[i].find_all('td',recursive=False)
     s = row[1].find_all('div',recursive=False)
     t = s[0].find_all('div',recursive=False)
     u = t[0].find_all('a',recursive=False)
     prob_name = u[0].get_text()
     maxx = max(len(prob_name),maxx)
    maxx+=1

    for i in range(1,l):
     a=chr(64+i)        #alphabet
     row = g[i].find_all('td',recursive=False)
     s = row[1].find_all('div',recursive=False)
     t = s[0].find_all('div',recursive=False)
     u = t[0].find_all('a',recursive=False)
     #no of successful submissions
     s1 =row[3].find_all('a',recursive=False)
     prob_name = u[0].get_text()
     prob_name = prob_name + " "*(maxx-len(prob_name))

     print(a,' : ',prob_name,' : ',s1[0].get_text())


    print("select one question you want to participate : ",end='')
    ques = input()
    a=ord(ques)
    if a>=97 and a<97+l:
            a=a-32

    if a>=65 and a<64+l:
            b=chr(a)
            link ="http://codeforces.com/contest/920/problem/"+b+""
            print(link)
    else:
            print("Please enter a question")

if(__name__=="__main__"):
    contest_num=920
    if(len(argv)==2):
        contest_num = argv[1]

    display_problems(contest_num)
