try:
    from util.Colour import Colour
    from util.Soup import get_soup
    from util.Contest import Contest
except:
    from Colour import Colour
    from Soup import get_soup
    from Contest import Contest

class Dummy_user:
    def __init__(self,uname):
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
        self.contests = []


    def init(self):
        self.fetch_data()


    def fetch_data(self):
        self.fetch_profile_data()
        self.fetch_contests_data()


    def fetch_profile_data(self):
        url = 'https://codeforces.com/profile/' + self.user_name
        soup = get_soup(url)
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
        url = 'http://codeforces.com/contests/with/'+uname
        soup = get_soup(url)
        if(soup is None):
            return

        if(not uname.lower() in soup.get_text().lower()):
            return

        table_rows = soup.findAll('table',{'class':'tablesorter'})[0].findAll('tr')[1:]
        contest_table = []
        for row in table_rows:
            num = row.findAll('td')[0].get_text().strip()
            contest = row.findAll('td')[1].get_text().strip()
            contest = Contest.get_short_contest_name(contest)
            link = row.findAll('td')[1].findAll('a')[0]['href'].strip().split('/')[-1]
            rank = row.findAll('td')[2].get_text().strip()
            solved = row.findAll('td')[3].get_text().strip()
            outof = Dummy_user.get_problem_num(link)
            rating_change = row.findAll('td')[4].get_text().strip()
            rating = row.findAll('td')[5].get_text().strip()
            change = row.findAll('td')[6].findAll('div')
            change = '' if len(change) == 0 else change[0].get_text().strip()
            contest_table.append([num,contest,rank,solved+"/"+outof,rating_change,rating,change,link])

        self.contests = contest_table


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
        from terminaltables import AsciiTable
        print(AsciiTable(table_data).table)


    def print_contests(self):
        '''
        print contests played by an user
        '''
        from terminaltables import AsciiTable
        table_data = [['num','contest','rank','done','change','rating','title-change','link']]
        table_data.extend(self.contests)
        print(AsciiTable(table_data).table)


    @staticmethod
    def _get_short_contest_name(contest):
        contest = contest.replace("Codeforces","CF")
        contest = contest.replace("Educational","EDU")
        contest = contest.replace("Rated","R")
        contest = contest.replace("rated","R")
        contest = contest.replace("Round","Rn")
        contest = contest.replace("Div. 2","D2")
        contest = contest.replace("Div. 1","D1")
        if(len(contest) > 30):
            contest = contest[0:30]
        return contest


    @staticmethod
    def get_problem_num(contest_num):
        return "-"
        # implementing caching else it is slow
        url = "https://codeforces.com/contest/"+contest_num
        soup = get_soup(url)
        if(soup is None):
            return

        prob_table = soup.findAll('table',{'class':'problems'})[0]
        prob_list = prob_table.findAll('tr')[1:]
        return str(len(prob_list))



if(__name__=="__main__"):
    uname='srbcheema1'
    from sys import argv
    if(len(argv)==2):
        uname = argv[1]
    dummy_user = Dummy_user(uname)
    dummy_user.fetch_data()
    dummy_user.print_data()
    dummy_user.print_contests()
