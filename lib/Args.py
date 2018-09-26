import os
import shutil

try:
    from lib.abs_path import abs_path
    from lib.Colour import Colour
    from lib.Constants import Const
    from lib.Contest import Contest
    from lib.files import verify_folder, verify_file
    from lib.Problem import Problem
    from lib.Runner import Runner
    from lib.srbjson import create_file, dump_data, extract_data
    from lib.global_config import get_contest_name, get_problem_name
except:
    from abs_path import abs_path
    from Colour import Colour
    from Constants import Const
    from Contest import Contest
    from files import verify_folder, verify_file
    from Problem import Problem
    from Runner import Runner
    from srbjson import create_file, dump_data, extract_data
    from global_config import get_contest_name, get_problem_name


def init_repo(args={},debug=False,init=False):
    '''
    initilize a repo as coolkit repo with default configuration
    if any parent repo is already initilized then we will just copy the config from there
    '''
    cwd = abs_path(os.getcwd())
    home_loc = abs_path('~')
    now = cwd
    while(now != home_loc):
        if('.coolkit' in os.listdir(now) and os.path.isdir(os.path.join(now,'.coolkit'))):
            if(debug): print('got .coolkit at ',now)
            break
        now = abs_path(os.path.join(now,os.pardir))
    if(now == home_loc):
        verify_folder(cwd+'/.coolkit/')
        create_file(cwd+'/.coolkit/config')
        print('initialized empty CoolKit repository in '+cwd+'/.coolkit/')
    elif(now != cwd):
        verify_folder(cwd+'/.coolkit/')
        shutil.copy(now+'/.coolkit/config',cwd+'/.coolkit/config')
        print(Colour.GREEN+'initialized empty CoolKit repository in '+cwd+'/.coolkit/'+Colour.END)
    else:
        if(init): print(Colour.YELLOW+'Already a coolkit repo'+Colour.END)

    if(not 'contest' in args or not args['contest']):
        contest_name = get_contest_name(cwd.split('/')[-1])
        if(not contest_name):
            args['contest'] = None
        else:
            args['contest'] = contest_name
    dump_data(args,cwd+'/.coolkit/config')


def set_local_config(args={},debug=False):
    '''
    set config to config file.
        parent config if found
        creates init if not
    '''
    if(not check_init()):
        init_repo()

    cwd = abs_path(os.getcwd())
    home_loc = abs_path('~')
    now = cwd
    while(now != home_loc):
        if('.coolkit' in os.listdir(now) and os.path.isdir(os.path.join(now,'.coolkit'))):
            if(debug): print('got .coolkit at ',now)
            break
        now = abs_path(os.path.join(now,os.pardir))

    dump_data(args,now+'/.coolkit/config')

def set_global_config(args={}):
    '''
    set config to global config file.
    '''
    dump_data(args,abs_path(Const.cache_dir + '/config'))


def check_init():
    '''
    set config to global config file.
    '''
    cwd = abs_path(os.getcwd())
    home_loc = abs_path('~')
    now = cwd
    while(now != home_loc):
        if('.coolkit' in os.listdir(now) and os.path.isdir(os.path.join(now,'.coolkit'))):
            return True
        now = abs_path(os.path.join(now,os.pardir))
    return False

def verify_init():
    if(not check_init()):
        print('not a coolkit repo')
        sys.exit(0)

def fetch_data_from_local_config():
    verify_init()
    cwd = abs_path(os.getcwd())
    home_loc = abs_path('~')
    now = cwd
    while(now != home_loc):
        if('.coolkit' in os.listdir(now) and os.path.isdir(os.path.join(now,'.coolkit'))):
            break
        now = abs_path(os.path.join(now,os.pardir))

    data = extract_data(now+'/.coolkit/config')
    return data

def fetch_contest(args):
    '''
    check cache
    '''
    c_name = str(args['contest'])
    temp_contest = Contest(c_name)
    if(not args['force'] and temp_contest.is_good):
        print(Colour.GREEN+'cache exists'+Colour.END)
        return
    temp_contest.fetch_contest()

def run(args):
    contest = Contest(args['contest'],args['type'])
    if(not contest.is_good):
        contest.fetch_contest()

    prob = Problem(args['contest'],args['prob'])
    if(not prob.is_good):
        print(Colour.YELLOW+'Test cases not found locally...'+Colour.END)
        # choice to fetch whole contest or problem
        prob.fetch_io()
        prob.dump_data()

    runner = Runner(args,prob)
    runner.run()


def submit_it(args):
    data = extract_data(Const.cache_dir+'/config')
    u_name = data['user']
    pswd = data['pswd']
    print(Colour.GREEN+'submitting %s file for %s prob on %s' % (args['inp'],args['prob'],args['contest']) +Colour.END)
