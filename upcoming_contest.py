import requests
import bs4
debug = False

def display_upcoming():
    if(not debug):
            req = requests.get("http://codeforces.com/contests")
            soup = bs4.BeautifulSoup(req.text,"html.parser")
    else:
            soup = bs4.BeautifulSoup(open("codeforces1.html"),"html.parser")

    a= soup.find_all(id='body')
    b=a[0].find_all('div',recursive=False)
    c=b[3].find_all('div',recursive=False)
    d=c[1].find_all('div',recursive=False)

    constestList = d[0]

    datatable,contesttable = constestList.find_all('div',recursive=False)
#all we need is datatable

    table_div=datatable.find_all('div',recursive=False)
    table = table_div[5].find_all('table',recursive=False)

    if(debug):
            tbody = table[0].find_all('tbody',recursive=False)[0]
            upcoming_contest = tbody.find_all('tr',recursive=False)[1:]
    else:
            upcoming_contest=table[0].find_all('tr',recursive=False)[1:]


    print("number of upcoming contests is",len(upcoming_contest))

#hurray we did it

    for contest in upcoming_contest:
            name_of_contest = contest.find_all('td',recursive=False)[0]
            contest_id = contest.get('data-contestid')
            print(" ",contest_id," : ",name_of_contest.get_text()[1:])

    print("select one contest you want to participate : ",end='')
    contest_id = str(input())

    link = "www.codeforces.com/contest/"+contest_id+""
    print(link)


if(__name__=="__main__"):
    display_upcoming()
