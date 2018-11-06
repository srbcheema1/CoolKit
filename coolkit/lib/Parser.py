import os
import sys

try:
    from argparse import ArgumentParser
    from argcomplete import autocomplete
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback,os
    sys.stderr.write(err)
    if(os.environ['HOME'] == 'srb'):
        traceback.print_exc()
    sys.exit(1)

from .. import __version__
from .Args import Args
from .Constants import Const
from .srbjson import srbjson

class Parser:
    @staticmethod
    def is_valid_file(parser, arg):
        if not os.path.exists(arg):
            parser.error("The file %s does not exist!" % arg)
        else:
            return arg

    @staticmethod
    def get_default(key,default_config):
        return default_config.get(key,None)

    @staticmethod
    def create_parser():
        default_config = srbjson.local_template['coolkit']
        if(Args.check_init()):
            default_config = Args.fetch_data_from_local_config()

        parser = ArgumentParser()
        parser.add_argument('-v',"--version",
                            action='store_true',
                            help="display version number")

        subparsers = parser.add_subparsers(dest='first_arg')

        # init
        '''
        init can have default values
        '''
        ini_parser = subparsers.add_parser('init')
        ini_parser.add_argument('-c',"--contest",
                                default = None,
                                help="contest num ex: 1080, 987, 840")
        ini_parser.add_argument('-t',"--type",
                                default = 'contest',
                                choices = ['contest','gym'],
                                help="contest type")
        ini_parser.add_argument('-p',"--prob",
                                default = 'A',
                                help="problem seq ex: A, B, C")
        ini_parser.add_argument('-s',"--site",
                                default='codeforces',
                                choices = ['codeforces'],
                                help="contest_site full link ex: codeforces")

        # set
        '''
        set should not have default values,
        its meaning less to have defaults in set
        '''
        set_parser = subparsers.add_parser('set')
        set_parser.add_argument('-c',"--contest",
                                help="contest num ex: 1080, 987, 840")
        set_parser.add_argument('-t',"--type",
                                choices = ['contest','gym'],
                                help="contest type")
        set_parser.add_argument('-p',"--prob",
                                help="problem seq ex: A, B, C")
        set_parser.add_argument('-s',"--site",
                                choices = ['codeforces'],
                                help="contest_site ex: codeforces")

        # run
        run_parser = subparsers.add_parser('run')
        run_parser.add_argument("inp",nargs='?',
                                type=lambda x: Parser.is_valid_file(run_parser,x),
                                default = Parser.get_default('inp',default_config),
                                help="input file ex: one.cpp")
        run_parser.add_argument('-t',"--test",
                                type=int,
                                default = -1, # -1 means all, 0 means custom
                                help="test case num")
        run_parser.add_argument('-p',"--prob",
                                # default = Parser.get_default('prob',default_config) # pick it from input_file name
                                default = None,
                                help="problem seq ex: A, B, C")

        # submit
        smt_parser = subparsers.add_parser('submit')
        smt_parser.add_argument("inp",nargs='?', # required
                                type=lambda x: Parser.is_valid_file(run_parser,x),
                                help="input file ex: one.cpp")
        smt_parser.add_argument('-p',"--prob",
                                # default = Parser.get_default('prob',default_config) # pick it from input_file name
                                default = None,
                                help="problem seq ex: A, B, C")
        smt_parser.add_argument('-f',"--force",
                                action='store_true',
                                default=False,
                                help="forcefully submit the file")
        smt_parser.add_argument("--force_stdout",
                                action='store_true',
                                default=False,
                                help="force verdict to stdout (not recommended)")

        # fetch
        '''
        this options should be availabe to be callable from anywhere
        no matter it is coolkit repo or not
        and it also doesn't create a new repo
        neither it sets values
        '''
        fch_parser = subparsers.add_parser('fetch')
        fch_parser.add_argument('-f',"--force",
                                action='store_true',
                                default=False,
                                help="forcefully fch contest")
        fch_parser.add_argument('-c',"--contest",
                                default = Parser.get_default('c_name',default_config),
                                help="contest num ex: 1080, 987, 840")
        fch_parser.add_argument('-t',"--type",
                                default = Parser.get_default('c_type',default_config),
                                choices = ['contest','gym'],
                                help="contest type")
        fch_parser.add_argument('-s',"--site",
                                default = Parser.get_default('c_site',default_config),
                                choices = ['codeforces'],
                                help="contest_site ex: codeforces")

        # config
        '''
        this is also same as fetch
        it wont create a new repo
        it will also not set values
        '''
        cfg_parser = subparsers.add_parser('config')
        cfg_parser.add_argument('-u',"--user",
                                    help="username/handle")
        cfg_parser.add_argument('-p',"--pswd",
                                    help="password")

        # view
        '''
        used to view contest, problem, user
        '''
        view_parser = subparsers.add_parser('view')
        view_subparsers = view_parser.add_subparsers(dest='second_arg')

        user_view_parser = view_subparsers.add_parser('user')
        user_view_parser.add_argument("u_name",nargs='?',
                                        default = None,
                                        help="username ex: srbcheema1")

        contest_view_parser = view_subparsers.add_parser('contest')
        contest_view_parser.add_argument("c_name",nargs='?',
                                        default = Parser.get_default('c_name',default_config),
                                        help="contest num ex: 1080, 987, 840")

        standings_view_parser = view_subparsers.add_parser('standings')
        standings_view_parser.add_argument("c_name",nargs='?',
                                        default = Parser.get_default('c_name',default_config),
                                        help="contest num ex: 1080, 987, 840")

        problem_view_parser = view_subparsers.add_parser('prob')
        problem_view_parser.add_argument("p_name",nargs='?',
                                        default = Parser.get_default('p_name',default_config),
                                        help="Problem name ex: A B C")

        view_subparsers.add_parser('upcoming')
        view_subparsers.add_parser('friends')


        autocomplete(parser)
        return parser

    @staticmethod
    def validate_args(args):
        if(args.version):
            print('coolkit '+__version__)
        return

