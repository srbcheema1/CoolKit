try:
    from util.Contest import Contest
    from util.Soup import get_soup
except:
    from Contest import Contest
    from Soup import get_soup

def display_upcoming():
    url = "http://codeforces.com/contests"
    soup = get_soup(url)

    contests = [['id','name','','time','dur.','link']]
    if(soup is None):
        return contests

    datatable = soup.find_all('div',{'class':'datatable'})[0].find_all('table')[0]
    contest_rows = datatable.find_all('tr')[1:]
    for row in contest_rows:
        c_id = row['data-contestid']
        data = row.find_all('td')
        name = data[0].get_text().strip()
        name = Contest.get_short_contest_name(name)
        writer = data[1].get_text().strip()
        time = data[2].get_text().strip()
        time = Contest.get_formatted_time(time)
        duration = data[3].get_text().strip()
        link = "www.codeforces.com/contest/"+c_id
        contests.append([c_id,name,writer,time,duration,link])

    return contests

if(__name__=="__main__"):
    contests = display_upcoming()
    from terminaltables import AsciiTable
    print(AsciiTable(contests).table)
