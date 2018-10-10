import os
import sys
import threading

try:
    from terminaltables import AsciiTable
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback,os
    sys.stderr.write(err)
    if(os.environ['HOME'] == 'srb'):
        traceback.print_exc()
    sys.exit(1)

from .Colour import Colour
from .utils import utils

class Runner:
    def __init__(self,args,prob):
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

        self.input_file = self.args['inp'].split('/')[-1]
        self.basename = self.input_file.split('.')[0]
        self.extension = self.input_file.split('.')[-1]
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

        self.comment_symbol = {
            'py': '# ',
            'rb': '# ',
            'c': '// ',
            'cpp': '// ',
            'java': '// ',
        }[self.extension]

    def run(self):
        if not self.extension in ['c', 'cpp', 'java', 'py', 'rb']:
            Colour.print('Supports only C, C++, Python, Java, and Ruby as of now.',Colour.RED)
            sys.exit(1)

        Runner.stamp_adder(self.input_file,self.comment_symbol + self.prob.link)

        if(self.args['test'] != 0):
            self._run_single_test(self.args['test'])
            return

        Colour.print('running %s file for %s prob on %s'%
                (self.args['inp'],self.args['p_name'],self.args['c_name']),Colour.GREEN)

        # COMPILE
        if not self.compiler is None:
            compile_status = os.system(self.compiler + ' \'' + self.input_file + '\'') #spaces in path
            if compile_status != 0:
                Colour.print('Compilation error.', Colour.RED)
                os.system(self.compiler + ' \'' + self.input_file + '\'') #spaces in path
                sys.exit(1)

        # RUN
        self._run_on_tests([test+1 for test in range(self.prob.num_test)])

    def _run_on_tests(self,tests):
        threads = []
        for i in tests:
            thread = threading.Thread(target=self._run_on_test,args=(i,))
            threads += [thread]
            thread.start()

        for x in threads:
            x.join()


    def _run_on_test(self,i):
            status = os.system('timeout 2s ' + self.execute_command + ' < ' + os.path.join(
                self.test_loc, 'Input' + str(i)) + ' > .coolkit/out_' + self.prob.p_name + str(i))

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

            if status == 0:
                # Ran successfully
                with open('.coolkit/out_'+ self.prob.p_name + str(i), 'r') as user_out_handler:
                    user_output = user_out_handler.read().strip().split('\n')
                    user_output = '\n'.join(
                        [line.strip() for line in user_output])
                    self.user_outputs[i] = user_output

                if orig_output == user_output:
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
        for i in range(1,self.prob.num_test+1):
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
        print(AsciiTable(table_data).table)
        if(self.bad_flag):
            Colour.print(self.prob.link, Colour.CYAN)
        if(self.prob.mult_soln):
            table_data = [
                    [Colour.PURPLE+'May contain multiple answers'+Colour.END],
                    [utils.shrink(self.prob.o_desc,80,[32])]
                ]
            print(AsciiTable(table_data).table)


    def _run_single_test(self,test):
        # COMPILE
        compiler = {
            'py': None,
            'rb': None,
            'c': 'gcc -static -g -fno-asm -lm -s -O2 -o .coolkit/' + self.basename+ '.out',
            'cpp': 'g++ -static -g -lm -s -x c++ -O2 -std=c++14 -o .coolkit/' + self.basename+'.out',
            'java': 'javac -d .'
        }[self.extension]
        if not self.compiler is None:
            compile_status = os.system(compiler + ' \'' + self.input_file + '\' > /dev/null 2>&1')
            if compile_status != 0:
                Colour.print('Compilation error.', Colour.RED)
                os.system(self.compiler + ' \'' + self.input_file + '\'') #spaces in path
                sys.exit(1)

        status = os.system(self.execute_command + ' < ' + os.path.join(self.test_loc, 'Input' + str(test)) )

    @staticmethod
    def stamp_adder(filename, line):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            lines = [x.strip() for x in f.readlines()]
            if(not line in lines):
                f.seek(0, 0)
                f.write(content + '\n' + line + '\n')
