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
    def __init__(self,c_name,c_type='contest',title=''):
        self.is_good = False # loaded fully or not
        self.title = title
        self.contest = str(c_name)
        self.c_type = c_type
        self.link = "https://codeforces.com/"+self.c_type+"/"+self.contest
        self.prob_mapp = {}
        self.prob_num = len(self.prob_mapp)
        self.dir = Const.cache_dir + '/' + self.c_type + '/' + self.contest

        dump_data({"contest":self.contest,"type":self.c_type}, self.dir+ "/config")
        self._load_contest()            # pick cached data
        # haven't called fetch_contest from constructor as it may be slow
        # call it seperately, its safe as it wont refetch things if loaded


    def fetch_contest(self,force=False):
        '''
        do fetching and dumping both
        '''
        if(not force and self.is_good):
            return

        self._fetch_problems_list()

        if (len(self.prob_mapp) == 0):
            print(Colour.RED+'unable to fetch problem list'+Colour.END)
            return

        prob_links = []
        p_names = []
        for key in self.prob_mapp.keys():
            if(force or not self.prob_mapp[key].is_good):
                prob_links.append(self.prob_mapp[key].link)
                p_names.append(key)

        # try to fetch
        failed_links,failed_p_names = self._fetch_prob_test_cases(prob_links,p_names)
        tries = 1
        while(len(failed_links) > 0 and tries > 0):
            failed_links,failed_p_names = self._fetch_prob_test_cases(failed_links,failed_p_names)
            print(Colour.YELLOW + tries+' try to fetch problems' + Colour.END)
            tries -= 1
        if(len(failed_links) > 0):
            for a in failed_p_names:
                print(Colour.RED + 'failed to fetch' + a + Colour.END)
            self.is_good = False
        else:
            self.is_good = True
        dump_data({"is_good":self.is_good,"contest":self.contest,"num_prob":self.prob_num}, self.dir+ "/config")


    def _fetch_prob_test_cases(self,links,p_names):
        """
        Method to download prob_test_cases for all problems
        """
        print(Colour.YELLOW + 'fetching problems ... ' + Colour.CYAN, p_names, Colour.END)

        rs = (grq.get(link) for link in links)
        responses = grq.map(rs)

        failed_probs = []
        failed_requests = []
        for response in responses:
            if response is not None and response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                prob = response.url.split('/')[-1]
                inputs, outputs, mult_soln = Problem.get_test_cases(soup,prob)

                if(len(inputs) == 0 or len(outputs) == 0 or len(inputs) != len(outputs)):
                    failed_requests += [response.url]
                    failed_probs += [prob]
                    continue

                self.prob_mapp[prob].inputs = inputs
                self.prob_mapp[prob].outputs = outputs
                self.prob_mapp[prob].mult_soln = mult_soln
                self.prob_mapp[prob].is_good = True
                self.prob_mapp[prob].num_test = len(inputs)
                self.prob_mapp[prob].dump_data()
            else:
                failed_requests += [response.url]
        return failed_requests,failed_probs


    def _load_contest(self):
        data = extract_data(self.dir+'/config')
        self.is_good = data['is_good']
        self.prob_num = data['num_prob']

        # problems
        path = self.dir + '/prob/'
        verify_folder(path)
        good_probs = 0
        prob_dirs = [ (a if os.path.isdir(path+a) else None) for a in os.listdir(path)]
        for a in prob_dirs:
            if(a):
                self.prob_mapp[a] = Problem(self.contest,a,self.c_type)
                if(self.prob_mapp[a].is_good):
                    good_probs += 1
                else:
                    self.is_good = False

        if(good_probs != self.prob_num):
            print(Colour.YELLOW+'expected',self.prob_num,'probs got',good_probs,'good probs',Colour.END)
            self.is_good = False
        if(self.prob_num == 0):
            print(Colour.YELLOW+'num_prob is 0 in config'+Colour.END)



    def display(self):
        self._display_prob_mapp()

    def _display_prob_mapp(self):
        table_data = [['#','Name','submissions','Link']]
        for prob in self.prob_mapp.values():
            table_data.append([prob.prob,prob.title,prob.subm,prob.link])
        print(AsciiTable(table_data).table)


    def _fetch_problems_list(self):
        soup = Soup.get_soup("https://codeforces.com/"+self.c_type+"/"+self.contest)

        if(soup is None):
            return

        prob_table = soup.findAll('table',{'class':'problems'})[0]
        prob_list = prob_table.findAll('tr')[1:]

        for problem in prob_list:
            prob = problem.findAll('td')[0].get_text().strip()
            title = problem.findAll('td')[1].findAll('a')[0].get_text().strip()
            subm = problem.findAll('td')[3].get_text().strip().split('x')[-1]
            if(not prob in self.prob_mapp.keys()):
                self.prob_mapp[prob] = Problem(self.contest,prob,self.c_type,title)
            self.prob_mapp[prob].title = title
            self.prob_mapp[prob].subm = subm
        self.prob_num = len(self.prob_mapp)
        dump_data({"num_prob":self.prob_num}, self.dir+ "/config")


    @staticmethod
    def upcoming_contest(display=False):
        url = "http://codeforces.com/contests"
        soup = Soup.get_soup(url)

        contests = [['id','title','','time','dur.','link']]
        if(soup is None):
            print(Colour.RED+'unable to fetch upcoming contests list'+Colour.END)
            return contests

        datatable = soup.find_all('div',{'class':'datatable'})[0].find_all('table')[0]
        contest_rows = datatable.find_all('tr')[1:]
        for row in contest_rows:
            c_id = row['data-contestid']
            data = row.find_all('td')
            title = data[0].get_text().strip()
            title = Contest.get_short_contest_title(title)
            writer = data[1].get_text().strip()
            time = data[2].get_text().strip()
            time = Contest.get_formatted_time(time)
            duration = data[3].get_text().strip()
            link = "www.codeforces.com/contest/"+c_id
            contests.append([c_id,title,writer,time,duration,link])

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
    def get_short_contest_title(contest):
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
    c_name="920"
    if(len(sys.argv)==2):
        c_name = sys.argv[1]

    temp_contest = Contest(c_name)
    temp_contest.fetch_contest()
    temp_contest.display()

    Contest.upcoming_contest(display=True)
