#! /usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import os
import sys

try:
    import getpass
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

from . import __version__
from .lib.Args import Args
from .lib.Colour import Colour
from .lib.Contest import Contest
from .lib.Friends import Friends
from .lib.Friends import Standing
from .lib.global_config import get_problem_name
from .lib.Parser import Parser
from .lib.Problem import Problem
from .lib.Profile import Dummy_user

coolkit_help="""usage coolkit [option] [--suboptions [args]]

options:
init        to initilize given folder as coolkit folder
set         to set values to various variables in .coolkit/config
run         to run a code against the sample testcases
fetch       to fetch data of a given contest
submit      to submit a problem
config      to configure username and password"""



def safe_main():
    parser = Parser.create_parser()
    pars_args = parser.parse_args()
    Parser.validate_args(pars_args)

    args = {}
    first_arg = pars_args.first_arg

    if(first_arg == "init"):
        '''
        initilize a repo as coolkit repo
        creates a .coolkit folder and a config file inside it.
        automatically detects contest name from foldername
        if parent repo is initilized then creates its ditoo copy of config
            parameters override
            contest name(overrides only if detected)
        '''
        args['c_name'] = pars_args.contest
        args['c_type'] = pars_args.type
        args['p_name'] = pars_args.prob
        args['c_site'] = pars_args.site
        Args.init_repo(args,init=True)

    elif(first_arg == "set"):
        '''
        just set values to config file in nearest ancestor coolkit directory
        doesn't initilize a repo as coolkit repo if any parent repo is already initilized.
        '''
        '''
        if condition required as it may or may not be given a value
        '''
        if(pars_args.contest): args['c_name'] = pars_args.contest
        if(pars_args.type): args['c_type'] = pars_args.type
        if(pars_args.prob): args['p_name'] = pars_args.prob
        if(pars_args.site): args['c_site'] = pars_args.site
        Args.set_local_config(args)

    elif(first_arg == "run"):
        '''
        runs the given problem.
        if no prob given it will check in cache.
        if no prob in cache then it will stop
        sets up cache for next time
        '''
        if(not Args.check_init()):
            Colour.print(Colour.YELLOW+'repo not found'+Colour.END)
            Args.init_repo()

        args['inp'] = pars_args.inp # can be none
        args['test'] = pars_args.test # 0 means all
        args['p_name'] = pars_args.prob # can be None

        config_data = Args.fetch_data_from_local_config()
        args['c_type'] = config_data['c_type'] # contest/gym
        args['c_name'] = config_data['c_name'] # can be None
        args['c_site'] = config_data['c_site'] # can be None

        if(not args['c_name']):
            Colour.print(Colour.RED+'contest not set, please set contest using `coolkit set -c <contest_num>`'+Colour.END)
            sys.exit(1)

        if(not args['inp']):
            Colour.print(Colour.RED+'no input file provided or found in cache'+Colour.END)
            sys.exit(1)

        if(not args['p_name']):
            Colour.print(Colour.YELLOW+"Prob name not provided, trying to detect from filename"+Colour.END)
            p = get_problem_name(args['inp'].split('/')[-1])
            if(p == None):
                Colour.print(Colour.YELLOW+"Unable to detect prob name from file name"+Colour.END)
                p = config_data['p_name']
            if(p == None):
                Colour.print(Colour.YELLOW+'No cached problem name found'+Colour.END)
                Colour.print(Colour.RED+'Please provide the problem name using -p option'+Colour.END)
                Args.set_local_config({'inp':args['inp']}) #cache up the input file for next turn
                sys.exit(1)
            args['p_name'] = p

        Args.set_local_config(args) #cache up the args for next turn
        Args.run(args)

    elif(first_arg == "submit"):
        if(not Args.check_init()):
            Args.init_repo()

        args['inp'] = pars_args.inp # can be None
        args['p_name'] = pars_args.prob # can be None

        config_data = Args.fetch_data_from_local_config()
        args['c_name'] = config_data['c_name'] # can be None
        args['c_type'] = config_data['c_type']
        args['c_site'] = config_data['c_site']

        if(not args['c_name']):
            Colour.print(Colour.RED+'contest not set, please set contest using `coolkit set -c <contest_num>`'+Colour.END)
            sys.exit(1)

        if(not args['inp']):
            Colour.print(Colour.RED+'no input file provided or found in cache'+Colour.END)
            sys.exit(1)

        if(not args['p_name']):
            Colour.print(Colour.YELLOW+"Prob name not provided, trying to detect from filename"+Colour.END)
            p = get_problem_name(args['inp'].split('/')[-1])
            if(p == None):
                Colour.print(Colour.YELLOW+"Unable to detect prob name from file name"+Colour.END)
                Colour.print(Colour.RED+'Please provide the problem name using -p option'+Colour.END)
                sys.exit(1)
            args['p_name'] = p

        config_data = Args.fetch_data_from_global_config()
        if(not config_data['user']):
            Colour.print(Colour.RED+'Please configure your username using "coolkit config -u <username>"'+Colour.END)
            config_data['user'] = input('Enter your username : ')
        if(not config_data['pswd']):
            Colour.print(Colour.YELLOW+'Please configure your password using "coolkit config -p <password>"'+Colour.END)
            config_data['pswd'] = getpass.getpass('Enter your password:')
        args['user'] = config_data['user']
        args['pswd'] = config_data['pswd']
        args['test'] = 0
        args['force'] = pars_args.force
        args['force_stdout'] = pars_args.force_stdout

        Args.submit_it(args)


    elif(first_arg == "fetch"):
        # Args.check_init() # fetching can be done even without this if contest name given
        args['c_name'] = pars_args.contest # can be None
        args['c_type'] = pars_args.type
        args['c_site'] = pars_args.site
        args['force'] = pars_args.force

        if(not args['c_name']):
            if(not Args.check_init()):
                Colour.print(Colour.RED+'no contest provided, either provide contest using -c or run command from a coolkit repo'+Colour.END)
                sys.exit(1)
            config_data = args.fetch_data_from_local_config()
            args['c_name'] = config_data['c_name'] # can be none
            if(not args['c_name']):
                Colour.print(Colour.RED+'contest not set, use `coolkit set -c <contest num>`, or provide contest name using -c parameter'+Colour.END)
                sys.exit(1)
        Args.fetch_contest(args)

    elif(first_arg == "config"):
        if(pars_args.user): args['user'] = pars_args.user
        if(pars_args.pswd): args['pswd'] = pars_args.pswd
        Args.set_global_config(args)

    elif(first_arg == "view"):
        second_arg = pars_args.second_arg

        if(second_arg == "user"):
            u_name = pars_args.u_name
            if(not u_name):
                u_name = input('Enter your username : ')
            dummy_user = Dummy_user(u_name,verbose=False)
            dummy_user.print_data()
            print(AsciiTable(dummy_user.contest_table).table)

        elif(second_arg == "contest"):
            c_name = pars_args.c_name
            if(not c_name):
                if(Args.check_init()):
                    Colour.print(Colour.YELLOW+'contest not set, use `coolkit set -c <contest num>`'+Colour.END)
                c_name = input('Enter contest name : ')

            temp_contest = Contest(c_name)
            temp_contest.pull_contest()
            temp_contest.display_contest()

        elif(second_arg == "standings"):
            c_name = pars_args.c_name
            if(not c_name):
                if(Args.check_init()):
                    Colour.print(Colour.YELLOW+'contest not set, use `coolkit set -c <contest num>`'+Colour.END)
                c_name = input('Enter contest name : ')

            config_data = Args.fetch_data_from_global_config()
            if(not config_data['user']):
                Colour.print(Colour.RED+'Please configure your username using "coolkit config -u <username>"'+Colour.END)
                config_data['user'] = input('Enter your username : ')
            if(not config_data['pswd']):
                Colour.print(Colour.YELLOW+'Please configure your password using "coolkit config -p <password>"'+Colour.END)
                config_data['pswd'] = getpass.getpass('Enter your password : ')

            temp_Standing = Standing(c_name,config_data['user'],config_data['pswd'])
            temp_Standing.show()

        elif(second_arg == "friends"):
            config_data = Args.fetch_data_from_global_config()
            if(not config_data['user']):
                Colour.print(Colour.RED+'Please configure your username using "coolkit config -u <username>"'+Colour.END)
                config_data['user'] = input('Enter your username : ')
            if(not config_data['pswd']):
                Colour.print(Colour.YELLOW+'Please configure your password using "coolkit config -p <password>"'+Colour.END)
                config_data['pswd'] = getpass.getpass('Enter your password : ')

            temp_friends = Friends(config_data['user'],config_data['pswd'])
            temp_friends.show()

        elif(second_arg == "prob"):
            if(not Args.check_init()):
                Colour.print(Colour.RED+'please run this command from a coolkit repo'+Colour.END)
                sys.exit(1)
            p_name = pars_args.p_name
            c_name = Args.fetch_data_from_local_config()['c_name']
            if(not c_name):
                Colour.print(Colour.YELLOW+'contest not set, use `coolkit set -c <contest num>`'+Colour.END)
                c_name = input('Enter contest name : ')
                Args.set_local_config({'c_name',c_name})
            if(not p_name):
                Colour.print(Colour.YELLOW+'problem not set, use `coolkit set -p <problem name>`'+Colour.END)
                p_name = input('Enter contest name : ')
                Args.set_local_config({'p_name',p_name})

            prob = Problem(p_name,c_name)
            prob.pull_problem(force=False)
            prob.display_problem()
            Colour.print(Colour.CYAN+prob.link+Colour.END)

        elif(second_arg == "upcoming"):
            Contest.upcoming_contest(display=True)

def main():
    try:
        safe_main()
    except KeyboardInterrupt:
        Colour.print('Exiting safely ... ')
        sys.exit(1)

if __name__ == '__main__':
    main()
