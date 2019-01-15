import pytest

import os
import random
import shutil


from srblib import show_dependency_error_and_exit
from srblib import remove
from srblib import abs_path
from srblib import on_travis

try:
    import getpass
except:
    show_dependency_error_and_exit()

from coolkit.lib.Args import Args
from coolkit.lib.Colour import Colour
from coolkit.lib.utils import utils

def test_Args():
    if not on_travis:
        return
    print()
    cwd = abs_path(os.getcwd())
    try:
        loc = cwd+'/test/contests/837'
        os.chdir(loc)
        remove(loc+'/.coolkit')

        args = {}
        args['c_name'] = '837'
        args['c_type'] = 'contest'
        args['p_name'] = None
        args['c_site'] = 'codeforces'
        Args.init_repo(args)
        print(Colour.CYAN+'Content of confing file'+Colour.END)
        os.system('cat '+loc+'/.coolkit/config')
        print(Colour.CYAN+'trying to init it again'+Colour.END)
        Args.init_repo(args)

        print(Colour.CYAN+'setting problem name to A'+Colour.END)
        Args.set_local_config({'p_name':'A'})
        print(Colour.CYAN+'Content of confing file'+Colour.END)
        os.system('cat '+loc+'/.coolkit/config')

        print(Colour.CYAN+'Deinitialize the folder'+Colour.END)
        remove(loc+'/.coolkit')

        print(Colour.CYAN+'Try to run the file'+Colour.END)
        os.system('coolkit run one.cpp')

        if(os.environ['USER'] == 'travis'):
            os.system('coolkit config --user coolkit --pswd coolkit')
        print(Colour.CYAN+'Try to submit wrong file'+Colour.END)
        os.system('coolkit submit three.cpp')

        if(utils.do_online_test()):
            print(Colour.CYAN+'Try to submit right file'+Colour.END)
            make_unique(loc)
            os.system('coolkit submit hidden_one.cpp')
            remove(loc+'/hidden_one.cpp')

        print(Colour.CYAN+'Deinitialize the folder'+Colour.END)
        remove(loc+'/.coolkit')

        remove('~/.config/coolkit/contest/222')
        print(Colour.CYAN+'Fetching some contest'+Colour.END)
        os.system('coolkit fetch -c 222 ')
        print(Colour.CYAN+'Fetching contest without force'+Colour.END)
        os.system('coolkit fetch -c 222')
        print(Colour.CYAN+'After making files defected'+Colour.END)
        os.remove(abs_path('~/.config/coolkit/contest/222/prob/A/io/Input1'))
        os.system('coolkit fetch -c 222')
        remove('~/.config/coolkit/contest/222')
        os.chdir(cwd)

    except Exception as e:
        # do clean up even in case of exception
        loc = cwd+'/test/contests/837'
        remove('~/.config/coolkit/contest/222')
        remove(loc+'/.coolkit')
        remove(loc+'/hidden_one.cpp')
        os.chdir(cwd)
        raise e


def make_unique(loc):
    '''
    utility function to make a file unique as never used before
    '''
    a = random.randint(1,10000000)
    a = random.randint(a,a+400)
    a = "// " + str(a) + " unique_id"
    shutil.copy(loc+'/one.cpp',loc+'/hidden_one.cpp')
    with open(loc+'/hidden_one.cpp', 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(content + a + '\n')
