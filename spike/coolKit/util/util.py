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


class Utilities:
    """
        set_contstants(mapp):
        check_cache(site, contest, problem):
        clear_cache(site):

        store_files(site, contest, problem, inputs, outputs):
        download_problem_testcases(args):
        download_contest_testcases(args):
        input_file_to_string(path, num_cases):
        cleanup(num_cases, basename, extension):
        handle_kbd_interrupt(site, contest, problem):
        get_html(url):
    """
    cache_dir = os.path.join(os.path.expanduser('~'), '.cache', 'coolkit') #cache
    colors = {
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'RED': '\033[91m',
        'ENDC': '\033[0m',
        'BOLD': '\033[1m',
    }

    @staticmethod
    def set_constants(mapp):
        """
        Utility method to set default site and contest
        """
        if(type(mapp) is not dict):
            print("required dictionary type argument")
            return

        with open(os.path.join(Utilities.cache_dir, 'constants.json'), 'r+') as f:
            data = f.read()
            data = json.loads(data)
            for key in mapp:
                data[key] = mapp[key]
            f.seek(0)
            f.write(json.dumps(data, indent=2))
            f.truncate()

        print 'Set %s to %s' % (key, value)

    @staticmethod
    def check_cache(site, contest, problem):
        """
        Method to check if the test cases already exist in cache
        If not, create the directory structure to store test cases
        """
        if os.path.isdir(os.path.join(Utilities.cache_dir, site, contest, problem)):
            return True
        else:
            os.makedirs(os.path.join(Utilities.cache_dir, site, contest, problem))
            return False

    @staticmethod
    def clear_cache(site):
        """
        Method to clear cached test cases
        """
        confirm = raw_input('Remove entire cache for site %s? (y/N) : ' % (site))
        if confirm == 'y':
            from shutil import rmtree
            try:
                rmtree(os.path.join(Utilities.cache_dir, site))
            except:
                print 'Some error occured. Try again.'
                return
            os.makedirs(os.path.join(Utilities.cache_dir, site))
            print 'Done.'

    @staticmethod
    def store_files(site, contest, problem, inputs, outputs):
        """
        Method to store the test cases in files
        """
        for i, inp in enumerate(inputs):
            filename = os.path.join(Utilities.cache_dir, site, contest, problem, 'Input' + str(i))
            with open(filename, 'w') as handler:
                handler.write(inp)

        for i, out in enumerate(outputs):
            filename = os.path.join(Utilities.cache_dir, site, contest, problem, 'Output' + str(i))
            with open(filename, 'w') as handler:
                handler.write(out)

    @staticmethod
    def download_problem_testcases(args):
        """
        Download test cases for a given problem
        """
        if args['site'] == 'codeforces':
            platform = Codeforces(args)
        elif args['site'] == 'codechef':
            platform = Codechef(args)
        else:
            platform = Hackerrank(args)

        is_in_cache = Utilities.check_cache(platform.site, platform.contest, platform.problem)

        if not args['force'] and is_in_cache:
            print 'Test cases found in cache...'
            sys.exit(0)

        platform.scrape_problem()

    @staticmethod
    def download_contest_testcases(args):
        """
        Download test cases for all problems in a given contest
        """
        if args['site'] == 'codeforces':
            platform = Codeforces(args)
        elif args['site'] == 'codechef':
            platform = Codechef(args)
        elif args['site'] == 'hackerrank':
            platform = Hackerrank(args)

        Utilities.check_cache(platform.site, platform.contest, platform.problem)
        platform.scrape_contest()

    @staticmethod
    def input_file_to_string(path, num_cases):
        """
        Method to return sample inputs as a list
        """
        inputs = []
        for i in xrange(num_cases):
            with open(os.path.join(path, 'Input' + str(i)), 'r') as fh:
                inputs += [fh.read()]
        return inputs

    @staticmethod
    def cleanup(num_cases, basename, extension):
        """
        Method to clean up temporarily created files
        """
        for i in xrange(num_cases):
            if os.path.isfile('temp_output' + str(i)):
                os.remove('temp_output' + str(i))
        if extension == 'java':
            os.system('rm ' + basename + '*.class')

    @staticmethod
    def handle_kbd_interrupt(site, contest, problem):
        """
        Method to handle keyboard interrupt
        """
        from shutil import rmtree
        print 'Cleaning up...'

        if problem is not None:
            path = os.path.join(Utilities.cache_dir, site, contest, problem)
            if os.path.isdir(path):
                rmtree(path)
        else:
            path = os.path.join(Utilities.cache_dir, site, contest)
            if os.path.isdir(path):
                rmtree(path)

        print 'Done. Exiting gracefully.'

    @staticmethod
    def get_html(url):
        """
        Utility function get the html content of an url
        """
        MAX_TRIES = 3
        try:
            for try_count in range(MAX_TRIES):
                r = rq.get(url)
                if r.status_code == 200:
                    break
            if try_count >= MAX_TRIES:
                print 'Could not fetch content. Please try again.'
                sys.exit(0)
        except Exception as e:
            print 'Please check your internet connection and try again.'
            sys.exit(0)
        return r
