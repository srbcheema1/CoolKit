import os
import shutil

from importlib.util import spec_from_file_location, module_from_spec

from srblib import abs_path, verify_file
from srblib import Module

from .Constants import Const

_path_of_default_global_config = '/'.join(abs_path(__file__).split('/')[:-2])+'/extra/global_config.py'
_global_config = Module(Const.cache_dir+'/global_config.py',_path_of_default_global_config)

def get_contest_name(folder):
    return _global_config.get_contest_name(folder)

def get_problem_name(file_name):
    return _global_config.get_problem_name(file_name)
