#!/usr/bin/env python3
import os
import sys

try:
    import grequests as grq
    from terminaltables import AsciiTable
    from bs4 import BeautifulSoup
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback
    traceback.print_exc()
    print(err)
    sys.exit(0)

try:
    from lib.Colour import Colour
    from lib.Constants import Const
    from lib.files import verify_folder, verify_file
    from lib.Problem import Problem
    from lib.Soup import Soup
    from lib.srbjson import dump_data, extract_data
except:
    from Colour import Colour
    from Constants import Const
    from files import verify_folder, verify_file
    from Problem import Problem
    from Soup import Soup
    from srbjson import dump_data, extract_data


class Contest:
    def __init__(self,c_num,name=None):
        if(name == None):
            name = ""
        self._init(c_num,name)

    def _init(self,c_num,name):
        # check for cached
        self.is_good = False
        self.name = name
        self.contest = str(c_num)
        self.link = "https://codeforces.com/contest/"+self.contest
        self.prob_mapp = {}
        self.prob_num = len(self.prob_mapp)
        if(os.path.exists(Const.cache_dir+'/contest'+self.contest)):
            self.load_contest()

    def fetch_contest(self,force=False):
        '''
        do fetching and dumping both
        '''
        if(not force and self.is_good):
            return
        self._fetch_problems()
        prob_links = []
        for key in self.prob_mapp.keys():
            prob_links.append(self.prob_mapp[key].link)

        # try to fetch
        failed = self._fetch_prob_test_cases(prob_links)
        tries = 1
        if(len(failed) > 0 and tries > 0):
            failed = self._fetch_prob_test_cases(links)
            print(Colour.YELLOW + tries+'th try to fetch problems' + Colour.END)
            tries -= 1
        if(len(failed) > 0):
            for a in failed:
                print(Colour.RED + 'failed to fetch' + a + Colour.END)
            self.is_good = False
        else:
            self.is_good = True
        dump_data({"is_good":self.is_good,"contest":self.contest,"num_prob":self.prob_num},
                Const.cache_dir + "/contest/" + self.contest + "/config")

    def _fetch_prob_test_cases(self,links):
        """
        Method to download prob_test_cases for all problems
        """
        print('fetching problems ... ')
        rs = (grq.get(link) for link in links)
        responses = grq.map(rs)

        failed_requests = []
        for response in responses:
            if response is not None and response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                seq = response.url.split('/')[-1]
                if(seq == ''):
                    print(response.url)
                inputs, outputs, mult_soln = Problem.get_test_cases(soup,seq)

                self.prob_mapp[seq].inputs = inputs
                self.prob_mapp[seq].outputs = outputs
                self.prob_mapp[seq].mult_soln = mult_soln
                self.prob_mapp[seq].is_good = True
                self.prob_mapp[seq].dump_io()
            else:
                failed_requests += [response.url]
        return failed_requests


    def load_contest(self):
        path = Const.cache_dir+'/contest/'
        data = extract_data(path+'config')
        self.is_good = data['is_good']
        self.prob_num = data['num_prob']

        # problems
        path = path + self.contest + '/'
        prob_dirs = [ (a if os.path.isdir(path+a) else None) for a in os.listdir(path)]
        for a in prob_dirs:
            if(a):
                self.prob_mapp[a] = Problem(self.contest,a)
                self.prob_mapp[a].load_problem()
                # TODO: inputs and outputs are yet to be fetched load_prob to be implemented

        self.prob_num = len(self.prob_mapp)


    def display(self):
        self.display_prob_mapp()


    def _display_prob_mapp(self):
        table_data = [['#','Name','submissions','Link']]
        for prob in self.prob_mapp.values():
            table_data.append([prob.seq,prob.name,prob.subm,prob.link])
        print(AsciiTable(table_data).table)

    def _fetch_problems(self):
        soup = Soup.get_soup("https://codeforces.com/contest/"+self.contest)

        if(soup is None):
            return

        prob_table = soup.findAll('table',{'class':'problems'})[0]
        prob_list = prob_table.findAll('tr')[1:]

        prob_mapp = {}
        for prob in prob_list:
            seq = prob.findAll('td')[0].get_text().strip()
            name = prob.findAll('td')[1].findAll('a')[0].get_text().strip()
            subm = prob.findAll('td')[3].get_text().strip().split('x')[-1]
            temp_prob = Problem(self.contest,seq,name)
            temp_prob.subm = subm
            prob_mapp[seq] = temp_prob
        self.prob_mapp = prob_mapp
        self.prob_num = len(prob_mapp)


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
    temp_contest._fetch_problems()
    temp_contest.display()

    Contest.upcoming_contest(display=True)
