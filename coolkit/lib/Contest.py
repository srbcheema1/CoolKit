#!/usr/bin/env python3
import os
import sys

try:
    import shutil
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

from .Colour import Colour
from .Constants import Const
from .files import verify_folder, verify_file
from .Problem import Problem
from .Soup import Soup
from .srbjson import srbjson
from .utils import utils


class Contest:
    def __init__(self,c_name,c_type='contest',c_title=''):
        # trivially cached
        self.c_name = str(c_name)
        self.c_type = c_type

        # fetchable variables
        self.announce_arr = []
        self.c_title = c_title
        self.hash = ""
        self.is_good = False # loaded fully or not
        self.num_prob = -1
        self.p_name_list = []

        # non cached
        self.dir = Const.cache_dir + '/' + self.c_type + '/' + self.c_name
        self.link = "https://codeforces.com/"+self.c_type+"/"+self.c_name
        self.prob_mapp = {}

        srbjson.dump_data({
                "c_name":self.c_name,
                "c_type":self.c_type
            },
            self.dir+ "/config",
            srbjson.contest_template)

        self._load_contest()            # pick cached data
        # haven't called fetch_contest from constructor as it may be slow
        # call it seperately, its safe as it wont refetch things if loaded

    def pull_contest(self,force=False):
        self.fetch_contest(force)
        self.dump_contest()

    def fetch_contest(self,force=False):
        '''
        do fetching and dumping both
        '''
        if(force): # remove every detail regarding that contest
            shutil.rmtree(self.dir)
            self._load_contest()
            self.prob_mapp = {}

        if(self.is_good): # return if cached
            return

        '''
        by now there is no useless folder and map entry
        '''
        self._fetch_contest_home()
        if (len(self.prob_mapp) == 0):
            print(Colour.RED+'failed to fetch contest home'+Colour.END)
            return

        '''
        by now there are only and all folders on all problems in contest
        and those folders are only and all mapped into prob_mapp

        missing entries are added by _fetch_contest_home()
        they might be bad or good depending on they are newly created or old ones respectively
        '''
        failed_links = []
        for key in self.p_name_list:
            if(not self.prob_mapp[key].is_good):
                failed_links.append(self.prob_mapp[key].link)

        '''
        only and only links to bad problems, empty folders exists for all
        '''
        tries = 1
        while(len(failed_links) > 0 and tries <= 2):
            print(Colour.YELLOW + str(tries)+': try to fetch problems' + Colour.END)
            failed_links = self._fetch_prob_test_cases(failed_links)
            tries += 1

        if(len(failed_links) > 0):
            for a in failed_links:
                print(Colour.RED + 'failed to fetch ' + a + Colour.END)
            self.is_good = False
        else:
            self.is_good = True


    def dump_contest(self):
        srbjson.dump_data({
                "ann_arr":self.announce_arr,
                "c_title":self.c_title,
                "is_good":self.is_good,
                "num_prob":self.num_prob,
                "p_name_list":self.p_name_list
            },
            self.dir+ "/config",
            srbjson.contest_template)

    def _fetch_prob_test_cases(self,links):
        """
        Method to download prob_test_cases for all problems
        """
        p_names = [ link.split('/')[-1] for link in links ]
        print(Colour.YELLOW + 'fetching problems ... ' + Colour.PURPLE, p_names, Colour.END)

        rs = (grq.get(link) for link in links)
        responses = grq.map(rs)

        failed_requests = []
        for response in responses:
            if response is not None and response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                p_name = response.url.split('/')[-1]
                self.prob_mapp[p_name].load_from_soup(soup)
                if(not self.prob_mapp[p_name].is_good):
                    failed_requests += [resopnse.url]
                    continue
                self.prob_mapp[p_name].dump_problem()
            else:
                failed_requests += [response.url]
        return failed_requests


    def _load_contest(self):
        '''
        loads contest from cache if exists else create an empty contest and loads it up
        also cleans useless folders in prob folder if they aren't in config of p_name_list
        '''
        data = srbjson.extract_data(self.dir+'/config',srbjson.contest_template)

        self.announce_arr = data['ann_arr']
        self.c_title = data['c_title']
        self.hash = data['hash']
        self.is_good = data['is_good']
        self.num_prob = data['num_prob']
        self.p_name_list = data['p_name_list']

        # problems
        path = self.dir + '/prob/'
        verify_folder(path)
        good_probs = 0
        prob_dir_list = [ (a if os.path.isdir(path+a) else None) for a in os.listdir(path)]
        prob_dirs = []
        for prob in prob_dir_list: # keep only folders
            if(prob): prob_dirs += [prob]

        for a in prob_dirs:
            self.prob_mapp[a] = Problem(a,self.c_name,self.c_type)
            if(self.prob_mapp[a].is_good and a in self.p_name_list): # remove waste folders
                good_probs += 1
            else:
                print(Colour.RED+'Removed Bad Problem : '+a+Colour.END)
                shutil.rmtree(self.prob_mapp[a].dir)
                del self.prob_mapp[a]

        if(self.num_prob == -1):
            print(Colour.YELLOW+'Contest not configured yet'+Colour.END)
            self.is_good = False
        elif(good_probs != self.num_prob):
            print(Colour.YELLOW+'expected',self.num_prob,'probs got',good_probs,'good probs',Colour.END)
            self.is_good = False



    def display_contest(self):
        table_data = [[Colour.BOLD+Colour.GREEN+self.c_title+Colour.END]]
        print(AsciiTable(table_data).table)
        table_data = [['#','Name','submissions','Link']]
        for prob in self.prob_mapp.values():
            table_data.append([prob.p_name,prob.p_title,prob.subm,prob.link])
        print(AsciiTable(table_data).table)
        table_data = [['S no','Announcements']]
        for a,ann in enumerate(self.announce_arr):
            table_data.append([a+1,utils.shrink(ann,max_len=80)])
        print(AsciiTable(table_data).table)



    def _fetch_contest_home(self):
        '''
        tries to fetch these things and also dump them if fetched
            contest:
                ann_arr
                c_title
                prob_mapp
                num_prob
                p_name_list

            problem:
                p_title
                subm

        CAN BE CALLED TO FORCEFULLY UPDATE DATA, say subm during the contest
        '''
        soup = Soup.get_soup("https://codeforces.com/"+self.c_type+"/"+self.c_name)

        if(soup is None):
            return

        # title
        rtable = soup.findAll('table',{'class':'rtable'})[0]
        self.c_title = rtable.findAll('a')[0].get_text().strip()

        # prob table
        prob_table = soup.findAll('table',{'class':'problems'})[0]
        prob_list = prob_table.findAll('tr')[1:]
        p_name_list = []

        for problem in prob_list:
            p_name = problem.findAll('td')[0].get_text().strip()
            p_name_list.append(p_name)
            p_title = problem.findAll('td')[1].findAll('a')[0].get_text().strip()
            subm = problem.findAll('td')[3].get_text().strip().split('x')[-1]
            if(not p_name in self.prob_mapp.keys()):
                self.prob_mapp[p_name] = Problem(p_name,self.c_name,self.c_type,p_title)
            self.prob_mapp[p_name].p_title = p_title
            self.prob_mapp[p_name].subm = subm
        self.num_prob = len(self.prob_mapp)
        self.p_name_list = p_name_list

        # announcements
        atable = soup.findAll('table',{'class':'problem-questions-table'})[0]
        announce_arr = atable.findAll('tr')[1:]
        for ann in announce_arr:
            ann = ann.findAll('td')[-1].get_text().strip()
            self.announce_arr += [ann]


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
            c_name = row['data-contestid']
            c_type = 'contests'
            data = row.find_all('td')
            title = data[0].get_text().strip()
            title = Contest.get_short_contest_title(title)
            title = utils.shrink(title)
            writer = data[1].get_text().strip()
            time = data[2].get_text().strip()
            time = Contest.get_formatted_time(time)
            duration = data[3].get_text().strip()
            link = "www.codeforces.com/"+c_type+"/"+c_name
            contests.append([c_name,title,writer,time,duration,link])

        if(display is True): print(AsciiTable(contests).table)
        return contests


    @staticmethod
    def get_number_of_problems(c_name,c_type='contest',cacheing=False):
        # TODO implementing caching else it is slow
        url = "https://codeforces.com/"+c_type+"/"+c_name
        soup = Soup.get_soup(url)
        if(soup is None):
            return "-",[]

        prob_table = soup.findAll('table',{'class':'problems'})[0]
        prob_list = prob_table.findAll('tr')[1:]

        p_name_list = []
        for problem in prob_list:
            p_name = problem.findAll('td')[0].get_text().strip()
            p_name_list += [p_name]

        return str(len(prob_list)) , p_name_list


    @staticmethod
    def get_short_contest_title(title):
        title = title.replace("Codeforces","CF")
        title = title.replace("Educational","EDU")
        title = title.replace("Elimination","ELM")
        title = title.replace("Rated","R")
        title = title.replace("rated","R")
        title = title.replace("Round","RnD")
        title = title.replace("round","RnD")
        title = title.replace("Div. 3","D3")
        title = title.replace("Div. 2","D2")
        title = title.replace("Div. 1","D1")
        title = title.replace("div. 3","D3")
        title = title.replace("div. 2","D2")
        title = title.replace("div. 1","D1")
        return title

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
    temp_contest.pull_contest()
    temp_contest.display_contest()

    Contest.upcoming_contest(display=True)
