#! /usr/bin/env python3
from functools import reduce
import os
import re

try:
	import texttable
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback
    traceback.print_exc()
    print(err)
    sys.exit(0)

try:
    from lib.Constants import Const
    from lib.files import verify_file
    from lib.Soup import Soup
except:
    from Constants import Const
    from files import verify_file
    from Soup import Soup

class Problem:
    def __init__(self,c_num,seq,name=""):
        self.seq = seq
        self.name = name
        self.contest = str(c_num)
        self.link = "https://codeforces.com/contest/"+self.contest+"/problem/"+self.seq
        self.subm = ""
        self.inputs = []
        self.outputs = []
        self.soup = None
        self.is_good = False
        self.mult_soln = False


    def dump_io(self):
        '''
        Dump the input output files
        '''
        for i, inp in enumerate(self.inputs):
            filename = os.path.join(Const.cache_dir + '/contest/' + self.contest , self.seq, 'Input' + str(i))
            verify_file(filename)
            with open(filename, 'w') as handler:
                handler.write(inp)

        for i, out in enumerate(self.outputs):
            filename = os.path.join(Const.cache_dir + '/contest/' + self.contest , self.seq, 'Output' + str(i))
            verify_file(filename)
            with open(filename, 'w') as handler:
                handler.write(out)


    def print_io(self):
        printer = [['#','input','output']]
        for i in range(len(self.inputs)):
            inp = self.inputs[i]
            out = self.outputs[i]
            printer.append([i+1,inp,out])

        tt = texttable.Texttable()
        tt.add_rows(printer)
        print(tt.draw())


    def _fetch_io(self):
        '''
        TODO: check for cached
        '''
        if(self.soup is None):
            self.soup = Soup.get_soup(self.link)

        if(self.soup is None):
            return

        self.inputs, self.outputs, self.mult_soln = Problem.get_test_cases(self.soup)

    @staticmethod
    def get_test_cases(soup,seq=''):
        """
        Method to parse the html and get test cases
        from a codeforces problem
        return formatted_inputs , formatted_outputs, mult_son

        TODO:
        implement sense of mult_soln
        """
        inputs = soup.findAll('div', {'class': 'input'})
        outputs = soup.findAll('div', {'class': 'output'})

        if len(inputs) == 0 or len(outputs) == 0:
            print('Problem not found.. '+seq)
            return [],[],False

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

        return formatted_inputs, formatted_outputs, False

if __name__ == "__main__":
    prob = Problem(1008,'C')
    prob._fetch_io()
    prob.print_io()
    print(prob.input)
