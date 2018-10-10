import os
import shutil
import sys

from .abs_path import abs_path
from .Colour import Colour
from .Constants import Const
from .Contest import Contest
from .files import verify_folder, verify_file
from .global_config import get_contest_name, get_problem_name
from .Problem import Problem
from .Runner import Runner
from .srbjson import srbjson
from .Submit import Submit

class Args:
    def init_repo(args={},debug=False,init=False):
        '''
        initilize a repo as coolkit repo with default configuration
        if any parent repo is already initilized then we will just copy the config from there
        '''
        cwd = abs_path(os.getcwd())
        home_loc = abs_path('~')
        root_loc = abs_path('/')
        now = cwd
        while(now != home_loc and now != root_loc):
            if('.coolkit' in os.listdir(now) and os.path.isdir(os.path.join(now,'.coolkit'))):
                if(debug): print('got .coolkit at ',now)
                break
            now = abs_path(os.path.join(now,os.pardir))
        if(now == root_loc):
            Colour.print('Coolkit should be run in path under home directory',Colour.RED)
            sys.exit(1)

        if(now == home_loc):
            verify_folder(cwd+'/.coolkit/')
            srbjson.create_file(cwd+'/.coolkit/config',srbjson.local_template)
            Colour.print('initialized empty CoolKit repository in '+cwd+'/.coolkit/',Colour.GREEN)
        elif(now != cwd):
            verify_folder(cwd+'/.coolkit/')
            shutil.copy(now+'/.coolkit/config',cwd+'/.coolkit/config')
            Colour.print('initialized empty CoolKit repository in '+cwd+'/.coolkit/',Colour.GREEN)
        else:
            if(init): Colour.print('Already a coolkit repo',Colour.YELLOW)

        if(not 'c_name' in args or not args['c_name']):
            contest_name = get_contest_name(cwd.split('/')[-1])
            if(not contest_name):
                args['c_name'] = None
            else:
                args['c_name'] = contest_name
        srbjson.dump_data(args,cwd+'/.coolkit/config',srbjson.local_template)


    def set_local_config(args={},debug=False):
        '''
        set config to config file.
            parent config if found
            creates init if not
        '''
        if(not Args.check_init()):
            Args.init_repo()

        cwd = abs_path(os.getcwd())
        home_loc = abs_path('~')
        root_loc = abs_path('/')
        now = cwd
        while(now != home_loc and now != root_loc):
            if('.coolkit' in os.listdir(now) and os.path.isdir(os.path.join(now,'.coolkit'))):
                if(debug): print('got .coolkit at ',now)
                break
            now = abs_path(os.path.join(now,os.pardir))
        if(now == root_loc):
            Colour.print('Coolkit should be run in path under home directory',Colour.RED)
            sys.exit(1)

        srbjson.dump_data(args,now+'/.coolkit/config',srbjson.local_template)

    def set_global_config(args={}):
        '''
        set config to global config file.
        '''
        srbjson.dump_data(args,abs_path(Const.cache_dir + '/config'),srbjson.global_template)


    def check_init():
        '''
        check if directory is initilized or not
        '''
        cwd = abs_path(os.getcwd())
        home_loc = abs_path('~')
        root_loc = abs_path('/')
        now = cwd
        while(now != home_loc and now != root_loc):
            if('.coolkit' in os.listdir(now) and os.path.isdir(os.path.join(now,'.coolkit'))):
                return True
            now = abs_path(os.path.join(now,os.pardir))
        if(now == root_loc):
            Colour.print('Coolkit should be run in path under home directory',Colour.RED)
            sys.exit(1)
        return False

    def get_init_path():
        '''
        set config to global config file.
        '''
        cwd = abs_path(os.getcwd())
        home_loc = abs_path('~')
        root_loc = abs_path('/')
        now = cwd
        while(now != home_loc and now != root_loc):
            if('.coolkit' in os.listdir(now) and os.path.isdir(os.path.join(now,'.coolkit'))):
                return now+'/.coolkit'
            now = abs_path(os.path.join(now,os.pardir))
        if(now == root_loc):
            Colour.print('Coolkit should be run in path under home directory',Colour.RED)
            sys.exit(1)
        return None

    def verify_init():
        if(not Args.check_init()):
            Colour.print('not a coolkit repo',Colour.RED)
            sys.exit(1)

    def fetch_data_from_local_config():
        Args.verify_init()
        cwd = abs_path(os.getcwd())
        home_loc = abs_path('~')
        root_loc = abs_path('/')
        now = cwd
        while(now != home_loc and now!= root_loc):
            if('.coolkit' in os.listdir(now) and os.path.isdir(os.path.join(now,'.coolkit'))):
                break
            now = abs_path(os.path.join(now,os.pardir))
        if(now == root_loc):
            Colour.print('Coolkit should be run in path under home directory',Colour.RED)
            sys.exit(1)

        data = srbjson.extract_data(now+'/.coolkit/config',srbjson.local_template)
        return data

    def fetch_data_from_global_config():
        data = srbjson.extract_data(abs_path('~/.config/coolkit/config'),srbjson.global_template)
        return data

    def fetch_contest(args):
        '''
        check cache
        '''
        c_name = str(args['c_name'])
        temp_contest = Contest(c_name)
        if(not args['force'] and temp_contest.is_good):
            Colour.print('cache exists',Colour.GREEN)
            return
        temp_contest.pull_contest(args['force'])


    def run(args):
        temp_contest = Contest(args['c_name'],args['c_type'])
        if(not temp_contest.is_good):
            temp_contest.pull_contest()


        temp_prob = Problem(args['p_name'],args['c_name'],args['c_type'])
        if(not temp_prob.is_good):
            Colour.print('Test cases not found locally...',Colour.YELLOW)
            # choice to fetch whole contest or problem
            temp_prob.pull_problem()

        if(not temp_prob.is_good):
            Colour.print('Sorry! Due to Connection problem. Unable to test your file',Colour.FULLRED)
            return

        runner = Runner(args,temp_prob,Args.get_init_path())
        runner.run()
        if(args['test']==0): # dont print table for single prob
            runner.print_table()


    def submit_it(args):
        data = srbjson.extract_data(Const.cache_dir+'/config',srbjson.global_template)
        u_name = data['user']
        pswd = data['pswd']

        if(not args['force']): # run only if it is not forced to submit
            temp_prob = Problem(args['p_name'],args['c_name'],args['c_type'])
            if(not temp_prob.is_good):
                Colour.print('Test cases not found locally...',Colour.YELLOW)
                # choice to fetch whole contest or problem
                temp_prob.pull_problem()

            if(not temp_prob.is_good):
                Colour.print('Sorry! Due to Connection problem. Unable to test your file',Colour.FULLRED)
                return

            runner = Runner(args,temp_prob,Args.get_init_path())
            runner.run()

        submit = Submit(args['c_name'],args['p_name'],args['inp'],args['user'],args['pswd'],args['force_stdout'])

        if(args['force']):
            submit.submit()
        elif(runner.result == 'GOOD'):
            submit.submit()
        elif(runner.result == 'CANT_SAY'):
            runner.print_table()
            submit.submit()
        else:
            Colour.print('ERROR locally, so wont upload faulty file',Colour.FULLRED)
            runner.print_table()
            if(args['force']): submit.submit()
