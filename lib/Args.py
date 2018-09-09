import os
import shutil

try:
    from lib.abs_path import abs_path
    from lib.Constants import Const
    from lib.files import verify_folder, verify_file
    from lib.srbjson import create_file, dump_data
    from lib.global_config import get_contest_name, get_problem_name
except:
    from abs_path import abs_path
    from Constants import Const
    from files import verify_folder, verify_file, dump_data
    from srbjson import create_file, dump_data
    from global_config import get_contest_name, get_problem_name


def init_repo(args={},debug=False):
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
        print('initialized empty CoolKit repository in '+cwd+'/.coolkit/')
    else:
        print('Already a coolkit repo')

    if('contest' not in args):
        contest_name = get_contest_name(cwd.split('/')[-1])
        if(contest_name != 'None'):
            args['contest'] = contest_name
    dump_data(args,cwd+'/.coolkit/config')


def set_local_config(args={},debug=False):
    '''
    set config to config file.
        parent config if found
        else it will create new one int this folder
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
        config_loc = cwd
        print('initialized empty CoolKit repository in '+config_loc+'/.coolkit/')
    elif(now != cwd):
        config_loc = now
    else:
        config_loc = cwd

    dump_data(args,config_loc+'/.coolkit/config')

def set_global_config(args={},debug=False):
    '''
    set config to global config file.
    '''
    dump_data(args,abs_path('~/.config/coolkit/config'))


def check_init(args={},debug=False):
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

def fetch_contest_name_from_config():
    cwd = abs_path(os.getcwd())
    home_loc = abs_path('~')
    now = cwd
    while(now != home_loc):
        if('.coolkit' in os.listdir(now) and os.path.isdir(os.path.join(now,'.coolkit'))):
            if(debug): print('got .coolkit at ',now)
            break
        now = abs_path(os.path.join(now,os.pardir))
    if(now == home_loc):
        return "None"

    data = extract_data(now+'/.coolkit/config')
    return data.get('contest')

def fetch_contest():
    '''
    check cache
    '''
    pass
