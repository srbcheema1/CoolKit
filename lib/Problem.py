#! /usr/bin/env python3
from functools import reduce
import re

try:
    from lib.Soup import Soup
except:
    from Soup import Soup

class Problem:
    def __init__(self,c_num,seq,name=""):
        self.seq = seq
        self.name = name
        self.contest = str(c_num)
        self.link = "https://codeforces.com/contest/"+self.contest+"/problem/"+self.seq
        self.subm = ""
        self.input = []
        self.output = []
        self.soup = None

    def fetch_test_cases(self):
        '''
        TODO: check for cached
        '''
        if(self.soup is None):
            self.soup = Soup.get_soup(self.link)

        if(self.soup is None):
            return

        self.input, self.output = Problem.get_test_cases(self.soup)

    def print_io(self):
        printer = [['#','input','output']]
        for i in range(len(self.input)):
            inp = self.input[i]
            out = self.output[i]
            printer.append([i+1,inp,out])

        import texttable
        tt = texttable.Texttable()
        tt.add_rows(printer)
        print(tt.draw())


    @staticmethod
    def get_test_cases(soup):
        """
        Method to parse the html and get test cases
        from a codeforces problem
        return formatted_inputs , formatted_outputs
        """
        inputs = soup.findAll('div', {'class': 'input'})
        outputs = soup.findAll('div', {'class': 'output'})

        if len(inputs) == 0 or len(outputs) == 0:
            print('Problem not found..')
            sys.exit(0)

        repls = ('<br>', '\n'), ('<br/>', '\n'), ('</br>', '')

        formatted_inputs, formatted_outputs = [], []
        for inp in inputs:
            pre = inp.find('pre').decode_contents()
            pre = reduce(lambda a, kv: a.replace(*kv), repls, pre)
            pre = re.sub('<[^<]+?>', '', pre)
            formatted_inputs += [pre]
        for out in outputs:
            pre = out.find('pre').decode_contents()
            pre = reduce(lambda a, kv: a.replace(*kv), repls, pre)
            pre = re.sub('<[^<]+?>', '', pre)
            formatted_outputs += [pre]

        return formatted_inputs, formatted_outputs

if __name__ == "__main__":
    prob = Problem(1008,'C')
    prob.fetch_test_cases()
    prob.print_io()
    print(prob.input)
