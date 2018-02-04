import requests
from bs4 import BeautifulSoup
from sys import argv
from lib.abs_path import abs_path
import os


def display_ques(prob_num='A'):
    pwd = str(os.getcwd())
    print(pwd)
    file_name = pwd+'/.config'
    file_name = abs_path(file_name)

    contest_num = str(920)

    req=requests.get('http://codeforces.com/contest/'+contest_num+'/problem/'+prob_num)
    soup=BeautifulSoup(req.text,'html.parser')

    a=soup.find_all(id='body')
    b=a[0].find_all('div',recursive=False)
#inside body
    c=b[3].find_all('div',recursive=False)
    d=c[1].find_all('div',recursive=False)
    e=d[1].find_all('div',recursive=False)
    f=e[0].find_all('div',recursive=False)
    g=f[0].find_all('div',recursive=False)
#reached to content

    h0=g[0].find_all('div',recursive=False)
#went under header
    print('Problem name : ',h0[0].get_text()[3:])
    print('')
#problem name printed

    h0[1]=h0[1].get_text()
    print('time limit per test :',h0[1][19:])
    print('')
#time printed

    print('memory limit per test :',h0[2].get_text()[21:])
    print('')
#memory printed

    print('Input :',h0[3].get_text()[5:])
    print('')
#input printed

    print('Output :',h0[4].get_text()[6:])
    print('')
#Output printed

    print('')
    print('Question :')

########
    image=g[1].find_all('img')
    if len(image)>0:
        print("Image",":",'http://codeforces.com/contest/'+contest_num+'/problem/'+prob_num)
#######
    h1=g[1].find_all('p',recursive=False)
    for i in range(0,len(h1)):
        print(h1[i].get_text())
#question printed
    print('')
    print('INPUT:')
    h2=g[2].find_all('p',recursive=False)
    for i in range(0,len(h2)):
        print(h2[i].get_text())
#input printed
    print('')
    print('OUTPUT:')
    h3=g[3].find_all('p',recursive=False)
    for i in range(0,len(h3)):
        print(h3[i].get_text(),end=('\n\n'))
#output printed

    h4=g[4].find_all('div',recursive=False)
    j=h4[1].find_all('div',recursive=False)
#inside sample test
    var=[]
    print('EXAMPLES')
    for k in range(0,len(j)):
     if (k+1)%2==0:
      print('Output')
     else:
      print('Input') 
     l=j[k].find_all('pre',recursive=False)


     var.insert(k,l[0].get_text('\n'))
     print(l[0].get_text('\n') )
     if k!=(len(j)-1):
      print('')
#Examples printed and variables stored ina list but it has \n character  

    print("TESTING")
    print(var)


if(__name__=="__main__"):
    prob_num = 'A'
    if(len(argv)==2):
            prob_num=argv[1]
    display_ques(prob_num)
