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
    from lib.Colour import Colour
    from lib.Constants import Const
    from lib.files import verify_file, verify_folder
    from lib.hash_dir import get_hash
    from lib.Soup import Soup
    from lib.srbjson import srbjson
except:
    from Colour import Colour
    from Constants import Const
    from files import verify_file, verify_folder
    from hash_dir import get_hash
    from Soup import Soup
    from srbjson import srbjson

class Problem:
    def __init__(self,p_name,c_name,c_type='contest',p_title="",subm=-1):
        self.p_title = p_title
        self.inputs = []
        self.outputs = []
        self.soup = None

        self.p_name = p_name            #config #required
        self.c_name = str(c_name)  #config #required
        self.c_type = c_type        #config #required

        self.num_test = 0           #config #to b fetched
        self.is_good = False        #config #to be fetched
        self.mult_soln = False      #config #to be fetched
        self.subm = subm            #config #to be fetched
        self.hash = ""              #config #to be fetched

        self.link = "https://codeforces.com/"+self.c_type+"/"+self.c_name+"/problem/"+self.p_name
        self.dir = Const.cache_dir + '/'+self.c_type+'/' + self.c_name + "/prob/" + self.p_name
        srbjson.dump_data({"c_name":self.c_name,"type":self.c_type,"p_name":self.p_name},
                self.dir + "/config",
                srbjson.prob_template)

        self._load_problem()


    def _load_problem(self):
        data = srbjson.extract_data(self.dir+'/config',srbjson.prob_template)
        self.is_good = data['is_good']
        self.num_test = data['num_test']
        self.mult_soln = data['mult_soln']
        self.hash = data['hash']
        self.p_title = data['p_title']
        self.subm = data['subm']
        verify_folder(self.dir + '/io')
        now_hash = get_hash(self.dir +'/io')
        if(self.hash != now_hash):
            print(Colour.YELLOW+'Warning prob '+self.p_name+' has been modified'+Colour.END)
            self.hash = now_hash
            srbjson.dump_data({"hash":self.hash}, self.dir + "/config",srbjson.prob_template)
        io = os.listdir(self.dir+'/io')
        if(len(io) != 2* self.num_test):
            if(len(io)!=0):
                print(Colour.RED+self.p_name + ' testcases corrupt' + str(io) + Colour.END)
            self.is_good = False
            srbjson.dump_data({"is_good":self.is_good}, self.dir + "/config",srbjson.prob_template)


    def dump_data(self):
        self._dump_io()
        now_hash = get_hash(self.dir +'/io')
        srbjson.dump_data({"is_good":self.is_good,"num_test":self.num_test,'subm':self.subm,
                "mul_soln":self.mult_soln,"hash":self.hash,"p_title":self.p_title},
                self.dir + "/config",
                srbjson.prob_template)


    def _dump_io(self):
        '''
        Dump the input output files
        '''
        for i, inp in enumerate(self.inputs):
            filename = os.path.join(self.dir, 'io', 'Input' + str(i+1))
            verify_file(filename)
            with open(filename, 'w') as handler:
                handler.write(inp)

        for i, out in enumerate(self.outputs):
            filename = os.path.join(self.dir, 'io', 'Output' + str(i+1))
            verify_file(filename)
            with open(filename, 'w') as handler:
                handler.write(out)


    def fetch_io(self,force=False):
        '''
        method to fetch io of a given problem
        we could fetch io for contest within contest.
        this method is to fetch io for individual problem
        '''
        if(not force and self.is_good):
            return

        if(self.soup is None):
            self.soup = Soup.get_soup(self.link)

        if(self.soup is None):
            print(Colour.RED+'failed to fetch problem'+Colour.END)
            return

        self.inputs, self.outputs, self.mult_soln = Problem.get_test_cases(self.soup)
        if(len(self.inputs) > 0 and len(self.outputs) > 0):
            if(len(self.inputs) == len(self.outputs)):
                self.is_good = True
                self.num_test = len(self.inputs)
            else:
                print(Colour.RED+'no of inputs unequal to no of outputs in problem'+Colour.END)


    def print_io(self):
        printer = [['#','input','output']]
        for i in range(len(self.inputs)):
            inp = self.inputs[i]
            out = self.outputs[i]
            printer.append([i+1,inp,out])

        tt = texttable.Texttable()
        tt.add_rows(printer)
        print(tt.draw())


    @staticmethod
    def get_test_cases(soup,p_name=''):
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
            print(Colour.RED+'Unable to fetch test cases in prob '+p_name + Colour.END)
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
    prob = Problem('C',1008)
    prob.fetch_io()
    prob.print_io()
    print(Colour.CYAN+prob.link+Colour.END)
