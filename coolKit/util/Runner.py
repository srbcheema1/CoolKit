import sys
import json
import re
import os
try:
    from bs4 import BeautifulSoup as bs
    import requests as rq
    import grequests as grq
    from argparse import ArgumentParser
except:
    err = """
    You haven't installed the required dependencies.
    Run 'python setup.py install' to install the dependencies.
    """
    print err
    sys.exit(0)

import Codeforces
import Codechef
import Hackerrank

def run_solution(args):
    """
    Method to run and test the user's solution against sample cases
    """
    problem = args['source']

    extension = problem.split('.')[-1]
    problem = problem.split('.')[0]
    basename = problem.split('/')[-1] # suppose we gave path folder/A.cpp
    problem_path = os.path.join(os.getcwd(), problem)

    if not os.path.isfile(problem_path + '.' + extension):
        print 'ERROR : No such file'
        sys.exit(0)

    problem_code = args['problem'] if args['problem'] else basename # A,B,C or codeforces
    contest_code = args['contest']

    testcases_path = os.path.join(Utilities.cache_dir, args['site'], contest_code, problem_code)

    if os.path.isdir(testcases_path):
        num_cases = len(os.listdir(testcases_path)) / 2
        results, expected_outputs, user_outputs = [], [], []

        if extension in ['c', 'cpp', 'java', 'py', 'hs', 'rb']:

            # Compiler flags taken from http://codeforces.com/blog/entry/79
            compiler = {
                'hs': 'ghc --make -O -dynamic -o ' + basename,
                'py': None,
                'rb': None,
                'c': 'gcc -static -DONLINE_JUDGE -fno-asm -lm -s -O2 -o ' + basename,
                'cpp': 'g++ -static -DONLINE_JUDGE -lm -s -x c++ -O2 -std=c++14 -o ' + basename,
                'java': 'javac -d .'
            }[extension]

            execute_command = {
                'py': 'python \'' + problem_path + '.' + extension + '\'',
                'rb': 'ruby \'' + problem_path + '.' + extension + '\'',
                'hs': './' + basename,
                'c': './' + basename,
                'cpp': './' + basename,
                'java': 'java -DONLINE_JUDGE=true -Duser.language=en -Duser.region=US -Duser.variant=US ' + basename
            }[extension]

            if compiler is None:
                compile_status = 0
            else:
                compile_status = os.system(compiler + ' \'' + problem_path + '.' + extension + '\'')#spaces in path

            if compile_status == 0:# Compiled successfully
                for i in xrange(num_cases):
                    status = os.system('timeout 2s ' + execute_command + ' < ' + os.path.join(
                        testcases_path, 'Input' + str(i)) + ' > temp_output' + str(i))

                    with open(os.path.join(testcases_path, 'Output' + str(i)), 'r') as out_handler:
                        expected_output = out_handler.read().strip().split('\n')
                        expected_output = '\n'.join(
                            [line.strip() for line in expected_output])
                        expected_outputs += [expected_output]

                        if status == 31744:
                            # Time Limit Exceeded
                            results += [Utilities.colors['BOLD'] + Utilities.colors[
                                'YELLOW'] + 'TLE' + Utilities.colors['ENDC']]
                            user_outputs += ['']

                        elif status == 0:
                            # Ran successfully
                            with open('temp_output' + str(i), 'r') as temp_handler:
                                user_output = temp_handler.read().strip().split('\n')
                                user_output = '\n'.join(
                                    [line.strip() for line in user_output])
                                user_outputs += [user_output]

                            if expected_output == user_output:
                                # All Correct
                                results += [Utilities.colors['BOLD'] + Utilities.colors[
                                    'GREEN'] + 'AC' + Utilities.colors['ENDC']]
                            else:
                                # Wrong Answer
                                results += [Utilities.colors['BOLD'] + Utilities.colors[
                                    'RED'] + 'WA' + Utilities.colors['ENDC']]

                        else:
                            # Runtime Error
                            results += [Utilities.colors['BOLD'] +
                                        Utilities.colors['RED'] + 'RTE' + Utilities.colors['ENDC']]
                            user_outputs += ['']
            else:# Compilation error occurred status = 1
                message = Utilities.colors['BOLD'] + Utilities.colors[
                    'RED'] + 'Compilation error. Not run against test cases' + Utilities.colors['ENDC'] + '.'
                print message
                sys.exit(0)

        else: #extension not in extensions
            print 'Supports only C, C++, Python, Java, Ruby and Haskell as of now.'
            sys.exit(0)

        from terminaltables import AsciiTable
        table_data = [['Serial No', 'Input',
                       'Expected Output', 'Your Output', 'Result']]
        inputs = Utilities.input_file_to_string(testcases_path, num_cases)
        for i in xrange(num_cases):
            row = [
                i + 1,
                inputs[i],
                expected_outputs[i],
                user_outputs[i] if any(sub in results[i] for sub in ['AC', 'WA']) else 'N/A',
                results[i]
            ]
            table_data.append(row)

        table = AsciiTable(table_data)
        print table.table

        # Clean up temporary files
        Utilities.cleanup(num_cases, basename, extension)

    else:
        print 'Test cases not found locally...'
        args['problem'] = problem_code
        args['force'] = True
        args['source'] = problem + '.' + extension

        Utilities.download_problem_testcases(args)

        print('Running your solution against sample cases...')
        run_solution(args)

