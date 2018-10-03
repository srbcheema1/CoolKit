#! /usr/bin/env python3
import sys

try:
    from terminaltables import AsciiTable
except:
    err = """
    You haven't installed the required dependencies.
    """
    print(err)
    sys.exit(0)

from .Soup import Soup
from .Colour import Colour
from .Contest import Contest

class Dummy_user:
    def __init__(self,uname):
        '''
        requires username as parameter. rest it will fetch online
        or from cached(to be implemented)
        '''
        self.user_name = uname
        self.link = 'https://codeforces.com/profile/'+self.user_name
        self.title = ""
        self.rating = ""
        self.max_rating = ""
        self.max_title = ""
        self.friends = ""
        self.reg_date = ""
        self.colour = ""
        self.div = ""
        self.contest_table = [['num','contest','rank','done','change','rating','title-change','link-num']]
        self.fetch_data()


    def fetch_data(self):
        '''
        TODO: implementing caching, only for offline
        '''
        self.fetch_profile_data()
        self.fetch_contests_data()


    def fetch_profile_data(self):
        url = 'https://codeforces.com/profile/' + self.user_name
        soup = Soup.get_soup(url)
        if(soup is None):
            return

        if(not uname.lower() in soup.get_text().lower()):
            return

        self.title = soup.find_all('div', {'class': 'user-rank'})[0].get_text().strip()

        info_div = soup.find_all('div', {'class': 'info'})[0].find_all('ul')[0].find_all('li')
        """
        0: ratings max and current
        2: friendds of n users
        4: registered when
        """
        self.rating = info_div[0].find_all('span')[0].get_text().strip()
        self.max_title = info_div[0].find_all('span')[1].find_all('span')[0].get_text().strip()[:-1]
        self.max_rating = info_div[0].find_all('span')[1].find_all('span')[1].get_text().strip()
        self.friends = info_div[2].get_text().strip().split(":")[-1].strip().split()[0]
        self.reg_date = info_div[4].find_all('span')[0].get_text().strip()

        self.colour = Colour.get_colour(self.title)
        self.div = 2
        if(int(self.rating) >= 1700):
            self.div = 1


    def fetch_contests_data(self):
        '''
        fetch data about contests played by the user
        '''
        url = 'http://codeforces.com/contests/with/'+uname
        soup = Soup.get_soup(url)
        if(soup is None):
            return

        if(not uname.lower() in soup.get_text().lower()):
            return

        table_rows = soup.findAll('table',{'class':'tablesorter'})[0].findAll('tr')[1:]
        contest_table = []
        for row in table_rows:
            num = row.findAll('td')[0].get_text().strip()
            c_title = row.findAll('td')[1].get_text().strip()
            c_title = Contest.get_short_contest_title(c_title)
            c_name = row.findAll('td')[1].findAll('a')[0]['href'].strip().split('/')[-1]
            rank = row.findAll('td')[2].get_text().strip()
            solved = row.findAll('td')[3].get_text().strip()
            outof , _p_name_list = Contest.get_number_of_problems(c_name)
            rating_change = row.findAll('td')[4].get_text().strip()
            rating = row.findAll('td')[5].get_text().strip()
            change = row.findAll('td')[6].findAll('div')
            change = '' if len(change) == 0 else change[0].get_text().strip()
            contest_table.append([num,c_title,rank,solved+"/"+outof,rating_change,rating,change,c_name])

        self.contest_table.extend(contest_table)


    def print_data(self):
        '''
        print data of user as displayed on his profile-page
        '''
        table_data = [[self.link]]
        table_data.append([self.colour + self.title + Colour.END])
        table_data.append([self.colour + self.user_name + Colour.END])
        table_data.append(['Contest rating: '+self.colour + self.rating + Colour.END +
            ' (max. ' + Colour.get_colour(self.max_title) + self.max_title + ',' + self.max_rating + Colour.END + ')'])
        table_data.append(['Friend of: ' + self.friends + ' users'])
        table_data.append(['Registered: '+self.reg_date])
        print(AsciiTable(table_data).table)



if(__name__=="__main__"):
    uname='srbcheema1'
    from sys import argv
    if(len(argv)==2):
        uname = argv[1]
    dummy_user = Dummy_user(uname)

    dummy_user.print_data()
    print(AsciiTable(dummy_user.contest_table).table)
