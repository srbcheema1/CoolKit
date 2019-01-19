import os
import sys
import threading

from srblib import abs_path, relative_path
from srblib import debug
from srblib import show_dependency_error_and_exit
from srblib import Tabular
from srblib import dump_output

from code_tester import comp_files

from .Colour import Colour
from .utils import utils


class Runner:
    def __init__(self,args,prob,cool_path):
        self.args = args
        self.prob = prob

        arr_len = self.prob.num_test + 1
        self.results = [''] * arr_len
        self.orig_inputs = [''] * arr_len
        self.orig_outputs = [''] * arr_len
        self.user_outputs = [''] * arr_len

        self.test_loc = self.prob.dir + '/io'
        self.bad_flag = False
        self.result = 'GOOD'

        self.cool_path = cool_path
        self.input_file = relative_path(self.args['inp'])
        self.basename = self.input_file.split('.')[0]
        self.extension = self.input_file.split('.')[-1]
        self.executable = self.cool_path + '/' + self.basename + '.out'

        if not self.extension in ['c', 'cpp', 'java', 'py', 'rb']:
            Colour.print('Supports only C, C++, Python, Java, and Ruby as of now.',Colour.RED)
            sys.exit(1)
        self.compiler = {
            'py': None,
            'rb': None,
            'c': 'gcc -static -DONLINE_JUDGE -g -fno-asm -lm -s -O2 -o ' + self.executable,
            'cpp': 'g++ -static -DONLINE_JUDGE -g -lm -s -x c++ -O2 -std=c++14 -o ' + self.executable,
            'java': 'javac -d .'
        }[self.extension]

        self.execute_command = {
            'py': 'python \'' + self.args['inp'] + '\'',
            'rb': 'ruby \'' + self.args['inp'] + '\'',
            'c': self.executable,
            'cpp': self.executable,
            'java': 'java -DONLINE_JUDGE=true -Duser.language=en -Duser.region=US -Duser.variant=US ' + self.basename
        }[self.extension]

        self.comment_symbol = {
            'py': '# ',
            'rb': '# ',
            'c': '// ',
            'cpp': '// ',
            'java': '// ',
        }[self.extension]

        self.now_loc = abs_path(os.getcwd())
        self.custom_testcases = False
        if(os.path.isfile(os.path.join(self.now_loc,"Input.txt")) and os.path.isfile(os.path.join(self.now_loc,"Output.txt"))):
            self.custom_testcases = True


    def run(self):
        Runner.stamp_adder(self.input_file,self.comment_symbol + self.prob.link)

        if(self.args['test'] != -1):
            self._run_single_test(self.args['test'])
            return

        Colour.print('running %s file for %s prob on %s'%
                (self.args['inp'],self.args['p_name'],self.args['c_name']),Colour.GREEN)

        # COMPILE
        if not self.compiler is None:
            if(debug): print(self.compiler + ' \'' + self.input_file + '\'') #spaces in path
            compile_status = os.system(self.compiler + ' \'' + self.input_file + '\'' + dump_output)
            if compile_status != 0:
                print(self.compiler + ' \'' + self.input_file + '\'') #spaces in path
                Colour.print('Compilation error.', Colour.RED)
                os.system(self.compiler + ' \'' + self.input_file + '\'') # prints twice
                sys.exit(1)

        # RUN
        self._run_on_tests([test+1 for test in range(self.prob.num_test)])

    def _run_on_tests(self,tests):
        threads = []
        for i in tests:
            thread = threading.Thread(target=self._run_on_test,args=(i,))
            threads += [thread]
            thread.start()

        if(self.custom_testcases):
            thread = threading.Thread(target=self._run_on_test,args=(0,))
            threads += [thread]
            thread.start()

        for x in threads:
            x.join()

    def _run_on_test(self,i):
        if(i==0):
            self._run_on_custom()
            return

        status = os.system('timeout 2s ' + self.execute_command + ' < ' + os.path.join(
            self.test_loc, 'Input' + str(i)) + ' > ' + self.cool_path + '/out_' + self.prob.p_name + str(i))

        with open(os.path.join(self.test_loc, 'Input' + str(i)), 'r') as in_handler:
            orig_input = in_handler.read().strip().split('\n')
            orig_input = '\n'.join(
                [line.strip() for line in orig_input])
            self.orig_inputs[i] = orig_input

        with open(os.path.join(self.test_loc, 'Output' + str(i)), 'r') as out_handler:
            orig_output = out_handler.read().strip().split('\n')
            orig_output = '\n'.join(
                [line.strip() for line in orig_output])
            self.orig_outputs[i] = orig_output

        if status == 31744:
            # Time Limit Exceeded
            self.results[i] = Colour.BOLD+Colour.YELLOW + 'TLE' +Colour.END
            self.user_outputs[i] = ''
            self.bad_flag = True
            self.result = 'BAD'

        elif status == 0:
            # Ran successfully
            with open(self.cool_path+'/out_'+ self.prob.p_name + str(i), 'r') as user_out_handler:
                user_output = user_out_handler.read().strip().split('\n')
                user_output = '\n'.join(
                    [line.strip() for line in user_output])
                self.user_outputs[i] = user_output

            orig_out_file = os.path.join(self.test_loc, 'Output' + str(i))
            user_out_file = self.cool_path+'/out_'+ self.prob.p_name + str(i)
            ret, size_diff = comp_files(orig_out_file,user_out_file)

            if ret == -1 and size_diff == False:
                # All Correct
                self.results[i] = Colour.BOLD+Colour.GREEN+ 'AC' +Colour.END
            elif self.prob.mult_soln:
                # Multiple possible
                self.results[i] = Colour.BOLD+Colour.CYAN+ 'Diff' +Colour.END
                if self.result == 'GOOD': self.result = 'CANT_SAY'
            else:
                # Wrong ans
                self.bad_flag = True
                self.results[i] = Colour.BOLD+Colour.DARKRED+ 'WA' +Colour.END
                self.result = 'BAD'
        else:
            # Runtime Error
            self.bad_flag = True
            self.results[i] = Colour.BOLD+Colour.FULLRED+ 'RTE' +Colour.END
            self.result = 'BAD'
            self.user_outputs[i] = ''


    def print_table(self):
        table_data = [['S No', 'Input',
                       'Orig Output', 'Your Output', 'Result']]
        first_test = 1
        if(self.custom_testcases): first_test = 0
        for i in range(first_test,self.prob.num_test+1):
            row = [
                i,
                self.orig_inputs[i],
                self.orig_outputs[i],
                self.user_outputs[i] if any(sub in self.results[i] for sub in ['AC', 'WA','Diff']) else 'N/A',
                self.results[i]
            ]
            table_data.append(row)
            table_data.append(['']*5)
        table_data.pop() # remove last empty line

        # small bug in Texttable while displaying Coloured output
        # tt = texttable.Texttable()
        # tt.add_rows(table_data)
        # print(tt.draw())
        print(Tabular(table_data))
        if(self.bad_flag):
            Colour.print(self.prob.link, Colour.CYAN)
        if(self.prob.mult_soln):
            table_data = [
                    [Colour.PURPLE+'May contain multiple answers'+Colour.END],
                    [utils.shrink(self.prob.o_desc,80,[32])]
                ]
            print(Tabular(table_data))


    def _run_on_custom(self,i=0):
        status = os.system('timeout 2s ' + self.execute_command + ' < ' + os.path.join(
            self.now_loc, 'Input.txt') + ' > ' + self.cool_path + '/out_' + self.prob.p_name + str(i))
        with open(os.path.join(self.now_loc, 'Input.txt'), 'r') as in_handler:
            orig_input = in_handler.read().strip().split('\n')
            orig_input = '\n'.join(
                [line.strip() for line in orig_input])
            self.orig_inputs[i] = orig_input
        with open(os.path.join(self.now_loc, 'Output.txt'), 'r') as out_handler:
            orig_output = out_handler.read().strip().split('\n')
            orig_output = '\n'.join(
                [line.strip() for line in orig_output])
            self.orig_outputs[i] = orig_output

        if status == 31744:
            self.results[i] = Colour.BOLD+Colour.YELLOW + 'TLE' +Colour.END
            self.user_outputs[i] = ''
        elif status == 0:
            with open(self.cool_path+'/out_'+ self.prob.p_name + str(i), 'r') as user_out_handler:
                user_output = user_out_handler.read().strip().split('\n')
                user_output = '\n'.join(
                    [line.strip() for line in user_output])
                self.user_outputs[i] = user_output

            orig_out_file = os.path.join(self.now_loc, 'Output.txt')
            user_out_file = self.cool_path+'/out_'+ self.prob.p_name + str(i)
            ret, size_diff = comp_files(orig_out_file,user_out_file)

            if ret == -1 and size_diff == False:
                self.results[i] = Colour.BOLD+Colour.GREEN+ 'AC' +Colour.END
            else:
                self.results[i] = Colour.BOLD+Colour.DARKRED+ 'WA' +Colour.END
        else:
            self.results[i] = Colour.BOLD+Colour.FULLRED+ 'RTE' +Colour.END
            self.user_outputs[i] = ''


    def _run_single_test(self,test):
        # COMPILE
        compiler = {
            'py': None,
            'rb': None,
            'c': 'gcc -static -g -fno-asm -lm -s -O2 -o ' + self.executable,
            'cpp': 'g++ -static -g -lm -s -x c++ -O2 -std=c++14 -o ' + self.executable,
            'java': 'javac -d .'
        }[self.extension]
        if not self.compiler is None:
            if(debug): print(self.compiler + ' \'' + self.input_file + '\'') #spaces in path
            compile_status = os.system(compiler + ' \'' + self.input_file + '\' ' + dump_output)
            if compile_status != 0:
                print(self.compiler + ' \'' + self.input_file + '\'') #spaces in path
                Colour.print('Compilation error.', Colour.RED)
                os.system(self.compiler + ' \'' + self.input_file + '\'') #spaces in path
                sys.exit(1)

        if(test == 0):
            if(os.path.isfile(os.path.join(self.now_loc,"Input.txt"))):
                os.system(self.execute_command + ' < ' + os.path.join(self.now_loc, 'Input.txt') )
            else:
                Colour.print('Please create Input.txt file in folder for custom test cases', Colour.RED)
        else:
            os.system(self.execute_command + ' < ' + os.path.join(self.test_loc, 'Input' + str(test)) )

    @staticmethod
    def stamp_adder(filename, line):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            lines = [x.strip() for x in f.readlines()]
            if(not line in lines):
                f.seek(0, 0)
                f.write(content + '\n' + line + '\n')
