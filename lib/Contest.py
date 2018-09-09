#!/usr/bin/env python3
import sys

try:
    from terminaltables import AsciiTable
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback
    traceback.print_exc()
    print(err)
    sys.exit(0)

try:
    from lib.Problem import Problem
    from lib.Soup import Soup
except:
    from Problem import Problem
    from Soup import Soup


class Contest:
    def __init__(self,c_num,name=None):
        if(name == None):
            name = ""
            # fetch name
        self.init(c_num,name)

    def init(self,c_num,name):
        # check for cached
        self.name = name
        self.contest = str(c_num)
        self.link = "https://codeforces.com/contest/"+self.contest
        self.prob_arr = []
        self.fetch_problems()
        self.no_probs = len(self.prob_arr)

    def display(self):
        self.display_prob_arr()

    def display_prob_arr(self):
        from terminaltables import AsciiTable
        table_data = [['#','Name','submissions','Link']]
        for prob in self.prob_arr:
            table_data.append([prob.seq,prob.name,prob.subm,prob.link])
        print(AsciiTable(table_data).table)

    def fetch_problems(self):
        contest_num = str(self.contest)
        soup = Soup.get_soup("https://codeforces.com/contest/"+contest_num)

        if(soup is None):
            return

        prob_table = soup.findAll('table',{'class':'problems'})[0]
        prob_list = prob_table.findAll('tr')[1:]

        prob_arr = []
        for prob in prob_list:
            seq = prob.findAll('td')[0].get_text().strip()
            name = prob.findAll('td')[1].findAll('a')[0].get_text().strip()
            subm = prob.findAll('td')[3].get_text().strip().split('x')[-1]
            temp_prob = Problem(seq,name)
            temp_prob.subm = subm
            temp_prob.contest_num = contest_num
            prob_arr.append(temp_prob)
        self.prob_arr = prob_arr

    @staticmethod
    def upcoming_contest(display=False):
        url = "http://codeforces.com/contests"
        soup = Soup.get_soup(url)

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

        if(display is True): print(AsciiTable(contests).table)
        return contests


    @staticmethod
    def get_number_of_problems(contest_num):
        return "-"
        # implementing caching else it is slow
        url = "https://codeforces.com/contest/"+contest_num
        soup = Soup.get_soup(url)
        if(soup is None):
            return

        prob_table = soup.findAll('table',{'class':'problems'})[0]
        prob_list = prob_table.findAll('tr')[1:]
        return str(len(prob_list))


    @staticmethod
    def get_short_contest_name(contest):
        contest = contest.replace("Codeforces","CF")
        contest = contest.replace("Educational","EDU")
        contest = contest.replace("Elimination","ELM")
        contest = contest.replace("Rated","R")
        contest = contest.replace("rated","R")
        contest = contest.replace("Round","RD")
        contest = contest.replace("Div. 2","D2")
        contest = contest.replace("Div. 1","D1")
        contest = contest.replace("[TBD]","D-")
        if(len(contest) > 30):
            contest = contest[0:30]
        return contest

    @staticmethod
    def get_formatted_time(time,offset = '03:00'):
        date,time = time.split()
        month,date = date.split('/')[:-1]
        date = int(date)

        hour,mins = time.split(':')
        hour = int(hour)
        mins = int(mins)

        off_h,off_m = offset.split(':')
        off_h = int(off_h)
        off_m = int(off_m)

        mins = mins + off_m
        if(mins >= 60):
            mins -= 60
            hour += 1

        hour = hour + off_h
        if(hour >= 24):
            hour -= 24
            date +=1

        return str(date).zfill(2) + '-' + month + ' ' + str(hour).zfill(2) + ':' + str(mins).zfill(2)

if(__name__=="__main__"):
    contest_num=920
    if(len(sys.argv)==2):
        contest_num = sys.argv[1]

    temp_contest = Contest(contest_num)
    temp_contest.fetch_problems()
    temp_contest.display()

    Contest.upcoming_contest(display=True)
