import os
import sys

try:
    from argparse import ArgumentParser
except:
    err = """
    You haven't installed the required dependencies.
    Run 'python setup.py install' to install the dependencies.
    """
    print(err)
    sys.exit(0)

from util.util import Utilities
from util.Runner import run_solution

supported_sites = ['codeforces', 'codechef', 'hackerrank']

def parse_flags(supported_sites):
    parser = ArgumentParser()

    parser.add_argument('-s', '--site',
                        dest='site',
                        choices=supported_sites,
                        help='The competitive programming platform, e.g. codeforces, codechef etc')
    parser.add_argument('-c', '--contest',
                        dest='contest',
                        help='The name of the contest, e.g. JUNE17, LTIME49, COOK83 etc')
    parser.add_argument('-p', '--problem',
                        dest='problem',
                        help='The problem code, e.g. OAK, PRMQ etc')
    parser.add_argument('-f', '--force',
                        dest='force',
                        action='store_true',
                        help='Force download the test cases, even if they are cached')
    parser.add_argument('--run',
                        dest='source_file',
                        help='Name of source file to be run')
    parser.add_argument('--set-default-site',
                        dest='default_site',
                        choices=supported_sites,
                        help='Name of default site to be used when -s flag is not specified')
    parser.add_argument('--set-default-contest',
                        dest='default_contest',
                        help='Name of default contest to be used when -c flag is not specified')
    parser.add_argument('--clear-cache',
                        dest='clear_cache',
                        action='store_true',
                        help='Clear cached test cases for a given site. Takes default site if -s flag is omitted')
    parser.add_argument('--init',
                        dest='init',
                        action='store_true',
                        help='init a directory with coolkit')

    parser.set_defaults(force=False, clear_cache=False)
    args = parser.parse_args()

    flags = {}

    # get cached
    import json
    site, contest = None, None
    try:
        with open(os.path.join(Utilities.cache_dir, 'constants.json'), 'r') as f:
            data = f.read()
        data = json.loads(data)
        site = data.get('default_site', None) if args.site is None else args.site
        contest = data.get('default_contest', None) if args.contest is None else args.contest
    except:
        print("unable to open constants.json")
        pass

    flags['site'] = site
    flags['contest'] = contest

    flags['problem'] = args.problem
    flags['force'] = args.force
    flags['clear_cache'] = args.clear_cache
    flags['source'] = args.source_file
    flags['default_site'] = args.default_site
    flags['default_contest'] = args.default_contest

    return flags


def validate_args(args):
    """
    Method to check valid combination of flags
    """
    if args['default_site'] != None or args['default_contest'] != None or args['clear_cache']:
        return
    if args['contest'] is None:
        print('Please specify contest code or set a default contest.')
        sys.exit(0)
    if args['source']:
        return


if __name__ == '__main__':
    args = parse_flags(supported_sites)
    validate_args(args)

    try:
        if args['default_site'] or args['default_contest']:
            Utilities.set_constants({'default_site':args['default_site'],'default_site':args['default_contest']})
        elif args['clear_cache']:
            Utilities.clear_cache(args['site'])
        elif args['source']:
            run_solution(args)
        elif args['problem'] is not None:
            Utilities.download_problem_testcases(args)
        elif args['contest']:
            Utilities.download_contest_testcases(args)
        else:
            print('Invalid combination of flags.')
    except KeyboardInterrupt:
        # Clean up files here
        Utilities.handle_kbd_interrupt(args['site'], args['contest'], args['problem'])
