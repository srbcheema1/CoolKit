import pytest
import os

from srblib import abs_path
from srblib import remove
from srblib import on_travis

from coolkit.lib.utils import utils

def test_view():
    if not on_travis:
        return
    print()
    cwd = abs_path(os.getcwd())
    try:
        loc = cwd+'/test/contests/837'
        os.chdir(loc)
        remove(loc+'/.coolkit')
        assert(os.system('coolkit init')==0)
        assert(os.system('coolkit view user srbcheema1')==0)
        assert(os.system('coolkit view contest')==0)
        assert(os.system('coolkit view prob A')==0)
        assert(os.system('coolkit view upcoming')==0)
        if(utils.do_online_test()):
            assert(os.system('coolkit view friends')==0)
            assert(os.system('coolkit view standings 935')==0)
        os.chdir(cwd)
    except Exception as e:
        remove(loc+'/.coolkit')
        os.chdir(cwd)
        raise e

