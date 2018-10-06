import os
import shutil
from importlib.util import spec_from_file_location, module_from_spec

from .abs_path import abs_path
from .Constants import Const
from .files import verify_file

def create_global_config():
    path_of_default_global_config = '/'.join(abs_path(__file__).split('/')[:-2])+'/extra/global_config.py'
    verify_file('~/.config/coolkit/global_config.py')
    shutil.copy(path_of_default_global_config, abs_path('~/.config/coolkit/global_config.py'))

# load file
def load_module(path):
    path = abs_path(path)
    if(not os.path.isfile(path)):
        create_global_config()
    mod_name = path.split('/')[-1].split('.')[0]

    global global_config
    spec = spec_from_file_location(mod_name,path)
    global_config = module_from_spec(spec)
    spec.loader.exec_module(global_config)

load_module(Const.cache_dir+'/global_config.py')

def get_contest_name(folder):
    return global_config.get_contest_name(folder)


def get_problem_name(file_name):
    return global_config.get_problem_name(file_name)
