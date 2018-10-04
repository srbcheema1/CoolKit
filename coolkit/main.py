#! /usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import os
import sys

try:
    import getpass
except:
    err = """
    You haven't installed the required dependencies.
    """
    print(err)
    sys.exit(0)

from .lib.Args import Args
from .lib.Parser import Parser
from .lib.Colour import Colour
from .lib.global_config import get_problem_name

coolkit_help="""usage coolkit [option] [--suboptions [args]]

options:
init        to initilize given folder as coolkit folder
set         to set values to various variables in .coolkit/config
run         to run a code against the sample testcases
fetch       to fetch data of a given contest
submit      to submit a problem
config      to configure username and password"""


def main():
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
            print(Colour.YELLOW+'repo not found'+Colour.END)
            Args.init_repo()

        args['inp'] = pars_args.inp # can be none
        args['test'] = pars_args.test # 0 means all
        args['p_name'] = pars_args.prob # can be None

        config_data = Args.fetch_data_from_local_config()
        args['c_type'] = config_data['c_type'] # contest/gym
        args['c_name'] = config_data['c_name'] # can be None
        args['c_site'] = config_data['c_site'] # can be None

        if(not args['c_name']):
            print(Colour.RED+'contest not set, please set contest using `coolkit set -c <contest_num>`'+Colour.END)
            sys.exit(0)

        if(not args['inp']):
            print(Colour.RED+'no input file provided or found in cache'+Colour.END)
            sys.exit(0)

        if(not args['p_name']):
            print(Colour.YELLOW+"Prob name not provided, trying to detect from filename"+Colour.END)
            p = get_problem_name(args['inp'].split('/')[-1])
            if(p == None):
                print(Colour.YELLOW+"Unable to detect prob name from file name"+Colour.END)
                p = config_data['p_name']
            if(p == None):
                print(Colour.YELLOW+'No cached problem name found'+Colour.END)
                print(Colour.RED+'Please provide the problem name using -p option'+Colour.END)
                Args.set_local_config({'inp':args['inp']}) #cache up the input file for next turn
                sys.exit(0)
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
            print(Colour.RED+'contest not set, please set contest using `coolkit set -c <contest_num>`'+Colour.END)
            sys.exit(0)

        if(not args['inp']):
            print(Colour.RED+'no input file provided or found in cache'+Colour.END)
            sys.exit(0)

        if(not args['p_name']):
            print(Colour.YELLOW+"Prob name not provided, trying to detect from filename"+Colour.END)
            print(args['inp'])
            p = get_problem_name(args['inp'].split('/')[-1])
            if(p == None):
                print(Colour.YELLOW+"Unable to detect prob name from file name"+Colour.END)
                print(Colour.RED+'Please provide the problem name using -p option'+Colour.END)
                sys.exit(0)
            args['p_name'] = p

        config_data = Args.fetch_data_from_global_config()
        if(not config_data['user']):
            print(Colour.RED+'Please configure your username using "coolkit config -u <username>"'+Colour.END)
            config_data['user'] = input('Enter your username : ')
        if(not config_data['pswd']):
            print(Colour.YELLOW+'Please configure your password using "coolkit config -p <password>"'+Colour.END)
            config_data['pswd'] = getpass.getpass('Enter your password:')
        args['user'] = config_data['user']
        args['pswd'] = config_data['pswd']
        args['test'] = 0
        args['force'] = pars_args.force

        Args.submit_it(args)


    elif(first_arg == "fetch"):
        # Args.check_init() # fetching can be done even without this if contest name given
        args['c_name'] = pars_args.contest # can be None
        args['c_type'] = pars_args.type
        args['c_site'] = pars_args.site
        args['force'] = pars_args.force

        if(not args['c_name']):
            if(not Args.check_init()):
                print(Colour.RED+'no contest provided, either provide contest using -c or run command from a coolkit repo'+Colour.END)
                sys.exit(0)
            else:
                config_data = Args.fetch_data_from_local_config()
                args['c_name'] = config_data['c_name'] # can be None
                print(Colour.RED+'contest not set, use `coolkit set -c <contest num>`, or provide contest name using -c parameter'+Colour.END)
                sys.exit(0)
        Args.fetch_contest(args)

    elif(first_arg == "config"):
        if(pars_args.user): args['user'] = pars_args.user
        if(pars_args.pswd): args['pswd'] = pars_args.pswd
        Args.set_global_config(args)


if __name__ == '__main__':
    main()
