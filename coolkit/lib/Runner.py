#!/usr/bin/env python3
import os
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

from .Colour import Colour
from .utils import utils

class Runner:
    def __init__(self,args,prob):
        self.args = args
        self.prob = prob
        self.results, self.orig_outputs, self.user_outputs = [], [], []
        self.test_loc = self.prob.dir + '/io'
        self.bad_flag = False
        self.input_file = self.args['inp'].split('/')[-1]
        self.basename = self.input_file.split('.')[0]
        self.extension = self.input_file.split('.')[-1]
        self.result = 'GOOD'
        self.compiler = {
            'py': None,
            'rb': None,
            'c': 'gcc -static -DONLINE_JUDGE -g -fno-asm -lm -s -O2 -o .coolkit/' + self.basename+ '.out',
            'cpp': 'g++ -static -DONLINE_JUDGE -g -lm -s -x c++ -O2 -std=c++14 -o .coolkit/' + self.basename+'.out',
            'java': 'javac -d .'
        }[self.extension]

        self.execute_command = {
            'py': 'python \'' + self.args['inp'] + '\'',
            'rb': 'ruby \'' + self.args['inp'] + '\'',
            'c': '.coolkit/' + self.basename+'.out',
            'cpp': '.coolkit/' + self.basename+'.out',
            'java': 'java -DONLINE_JUDGE=true -Duser.language=en -Duser.region=US -Duser.variant=US ' + self.basename
        }[self.extension]

    def run(self):
        if not self.extension in ['c', 'cpp', 'java', 'py', 'rb']:
            print(Colour.CYAN+'Supports only C, C++, Python, Java, and Ruby as of now.'+Colour.END)
            sys.exit(0)

        if(self.args['test'] != 0):
            self._run_single_test(self.args['test'])
            return

        print(Colour.GREEN+'running %s file for %s prob on %s'%
                (self.args['inp'],self.args['p_name'],self.args['c_name'])+Colour.END)

        # COMPILE
        if not self.compiler is None:
            compile_status = os.system(self.compiler + ' \'' + self.input_file + '\'') #spaces in path
            if compile_status != 0:
                print(Colour.RED + 'Compilation error.' + Colour.END)
                os.system(self.compiler + ' \'' + self.input_file + '\'') #spaces in path
                sys.exit(0)

        # RUN
        self._run_on_tests([test+1 for test in range(self.prob.num_test)])


    def print_table(self):
        table_data = [['S No', 'Input',
                       'Orig Output', 'Your Output', 'Result']]
        inputs = Runner._input_file_to_string(self.test_loc, self.prob.num_test)
        for i in range(self.prob.num_test):
            row = [
                i + 1,
                inputs[i],
                self.orig_outputs[i],
                self.user_outputs[i] if any(sub in self.results[i] for sub in ['AC', 'WA']) else 'N/A',
                self.results[i]
            ]
            table_data.append(row)

        # small bug in Texttable while displaying Coloured output
        # tt = texttable.Texttable()
        # tt.add_rows(table_data)
        # print(tt.draw())
        print(AsciiTable(table_data).table)
        if(self.bad_flag):
            print(Colour.CYAN + self.prob.link + Colour.END)
        if(self.prob.mult_soln):
            table_data = [
                    [Colour.PURPLE+'May contain multiple answers'+Colour.END],
                    [utils.shrink(self.prob.o_desc,80,[32])]
                ]
            print(AsciiTable(table_data).table)


    def _run_on_tests(self,tests):
        for i in tests:
            status = os.system('timeout 2s ' + self.execute_command + ' < ' + os.path.join(
                self.test_loc, 'Input' + str(i)) + ' > .coolkit/out_' + self.prob.p_name + str(i))

            with open(os.path.join(self.test_loc, 'Output' + str(i)), 'r') as out_handler:
                orig_output = out_handler.read().strip().split('\n')
                orig_output = '\n'.join(
                    [line.strip() for line in orig_output])
                self.orig_outputs += [orig_output]

            if status == 31744:
                # Time Limit Exceeded
                self.results += [Colour.BOLD+Colour.YELLOW + 'TLE' +Colour.END]
                self.user_outputs += ['']
                self.bad_flag = True
                self.result = 'BAD'

            if status == 0:
                # Ran successfully
                with open('.coolkit/out_'+ self.prob.p_name + str(i), 'r') as user_out_handler:
                    user_output = user_out_handler.read().strip().split('\n')
                    user_output = '\n'.join(
                        [line.strip() for line in user_output])
                    self.user_outputs += [user_output]

                if orig_output == user_output:
                    # All Correct
                    self.results += [Colour.BOLD+Colour.GREEN+ 'AC' +Colour.END]
                elif self.prob.mult_soln:
                    # Multiple possible
                    self.results += [Colour.BOLD+Colour.CYAN+ 'Diff' +Colour.END]
                    if self.result == 'GOOD': self.result = 'CANT_SAY'
                else:
                    # Wrong ans
                    self.bad_flag = True
                    self.results += [Colour.BOLD+Colour.DARKRED+ 'WA' +Colour.END]
                    self.result = 'BAD'
            else:
                # Runtime Error
                self.bad_flag = True
                self.results += [Colour.BOLD+Colour.FULLRED+ 'RTE' +Colour.END]
                self.result = 'BAD'
                self.user_outputs += ['']


    def _run_single_test(self,test):
        # COMPILE
        if not self.compiler is None:
            compile_status = os.system(self.compiler + ' \'' + self.input_file + '\' > /dev/null 2>&1') #spaces in path
            if compile_status != 0:
                print(Colour.RED + 'Compilation error.' + Colour.END)
                os.system(self.compiler + ' \'' + self.input_file + '\'') #spaces in path
                sys.exit(0)

        status = os.system(self.execute_command + ' < ' + os.path.join(self.test_loc, 'Input' + str(test)) )

    @staticmethod
    def _input_file_to_string(path, num_cases):
        """
        Method to return sample inputs as a list
        """
        inputs = []
        for i in range(num_cases):
            with open(os.path.join(path, 'Input' + str(i+1)), 'r') as fh:
                inputs += [fh.read()]
        return inputs

