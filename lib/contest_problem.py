import requests
import bs4
from sys import argv

class Problem:
    def __init__(self,seq,name,subm,c_num):
        self.seq = seq
        self.name = name
        self.subm = subm
        self.contest = str(c_num)
        self.link = "https://codeforces.com/contest/"+self.contest+"/problem/"+self.seq


class Contest:
    def __init__(self,c_num,name):
        init(c_num,name)

    def __init__(self,c_num):
        name = ""
        # fetch name
        init(c_num,name)

    def init(self,c_num,name):
        # check for cached
        self.name = name
        self.contest = str(c_num)
        self.link = "https://codeforces.com/contest/"+self.contest
        self.prob_arr = Contest.fetch_problems(self.contest)

    def display(self):
        Contest.display(self.prob_arr)

    @staticmethod
    def display(prob_arr):
        from terminaltables import AsciiTable
        table_data = [['#','Name','submissions','Link']]
        for prob in prob_arr:
            table_data.append([prob.seq,prob.name,prob.subm,prob.link])
        print(AsciiTable(table_data).table)


    @staticmethod
    def fetch_problems(contest_num):
        contest_num = str(contest_num)
        req=requests.get("https://codeforces.com/contest/"+contest_num)
        soup = bs4.BeautifulSoup(req.text,"html.parser")

        prob_table = soup.findAll('table',{'class':'problems'})[0]
        prob_list = prob_table.findAll('tr')[1:]

        prob_arr = []
        for prob in prob_list:
            seq = prob.findAll('td')[0].get_text().strip()
            name = prob.findAll('td')[1].findAll('a')[0].get_text().strip()
            subm = prob.findAll('td')[3].get_text().strip().split('x')[-1]
            prob_arr.append(Problem(seq,name,subm,contest_num))
        return prob_arr


if(__name__=="__main__"):
    contest_num=920
    if(len(argv)==2):
        contest_num = argv[1]

    prob_arr = Contest.fetch_problems(contest_num)
    Contest.display(prob_arr)
